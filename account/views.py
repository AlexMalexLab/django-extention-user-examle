import os
from urllib.parse import urlparse
from urllib.request import urlretrieve
import uuid

import httplib2
from googleapiclient.discovery import build as google_api_build
import facebook

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.core.files import File

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import list_route
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.authtoken.models import Token


from .serializers import LoginSerializer, UserSerializer, RetrieveUserSerializer, RestoreAccessSerializer
from .models import ExtUser
from .flows import get_all_flows, get_flow


class Login(TemplateView):
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['oauth_url'] = get_all_flows()
        return context


class Registration(TemplateView):
    template_name = 'account/registration.html'


class RestoreAccess(TemplateView):
    template_name = 'account/restore_access.html'


class Profile(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usr_id'] = self.request.user.id
        return context

    template_name = 'account/profile.html'


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk


class UserViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = ExtUser.objects.all()
    action_serializer_classes = {
        'create': UserSerializer,
        'update': UserSerializer,
        'partial_update': UserSerializer,
        'retrieve': RetrieveUserSerializer,
        'restore_access': RestoreAccessSerializer,
        'login': LoginSerializer,
    }

    def perform_create(self, serializer):
        instance = serializer.save()
        login(self.request, instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        login(self.request, instance)

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [permissions.IsAuthenticated(), IsOwner()]

        return [permissions.AllowAny()]

    @list_route(methods=['post'])
    def restore_access(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, username=serializer.data.get('login'), password=serializer.data.get('password'))
        if user:
            login(request, user)
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response({'id': user.pk, 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {api_settings.NON_FIELD_ERRORS_KEY: _('Такой пользователь не найден')},
                status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['post', 'get'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        Token.objects.filter(user=self.request.user).delete()
        logout(request)
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)


def auth_by_token(request, token):
    token = Token.objects.filter(pk=token)
    if token:
        login(request, token.get().user)
        return redirect('account:profile')
    else:
        return redirect('account:login')


# Get oauth token of social network and login or create and login
def oauth(request, mode):
    flow = get_flow(mode)

    try:
        code = request.GET['code']
        credentials = flow.step2_exchange(code)
        #print(credentials.access_token)
        social_data = {'email': None, 'name': None, 'picture': None}

        # Get social data from access_token
        if mode == 'google':
            # https://developers.google.com/oauthplayground
            # https://google-api-client-libraries.appspot.com/documentation/oauth2/v2/python/latest/index.html
            # https://developers.google.com/api-client-library/python/apis/
            http = httplib2.Http()
            http = credentials.authorize(http)
            service = google_api_build('oauth2', 'v2', http=http)
            data = service.userinfo().v2().me().get().execute()
            social_data = {
                'email': data['email'],
                'name': data['name'],
                'picture': data.get('picture')
            }
        elif mode == 'facebook':
            graph = facebook.GraphAPI(access_token=credentials.access_token)
            data = graph.get_object("me?fields=name,email")
            data_dict = dict(data)
            social_data = {
                'email': data['email'],
                'name': data['name'],
            }
        else:
            raise Exception

        if not social_data['email']:
            raise Exception

        try:
            user = ExtUser.objects.get(login=social_data['email'])
            login(request, user)
        except ObjectDoesNotExist:
            open_password = str(uuid.uuid1())
            data = {
                'login': social_data['email'],
                'password': open_password,
                'password_confirm': open_password,
                'name': social_data['name']
            }
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            login(request, user)

        if social_data.get('picture') and not user.avatar:
            url = social_data['picture']
            img_name = os.path.basename(urlparse(url).path)
            local_filename, headers = urlretrieve(url)
            with open(local_filename, 'rb') as f:
                user.avatar.save(img_name, File(f), save=True)

        return redirect('account:profile')
    except:
        #raise Exception
        return redirect('account:login')

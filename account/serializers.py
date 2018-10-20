from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from mail_templated import send_mail

from .models import ExtUser


class LoginSerializer(serializers.ModelSerializer):
    login = serializers.EmailField(required=True, max_length=150)

    class Meta:
        model = ExtUser
        fields = ('login', 'password')


class RetrieveUserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateTimeField(format='%d/%m/%Y')
    class Meta:
        model = ExtUser
        exclude = ('password', )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    password_confirm = serializers.CharField(max_length=128, allow_blank=False, write_only=True)

    class Meta:
        model = ExtUser
        fields = ('id', 'login', 'name', 'password', 'password_confirm',
                  'birthday', 'country',  'city', 'interests', 'ya_purse', 'avatar')

    def create(self, validated_data):
        data = validated_data
        del data['password_confirm']
        user = ExtUser.objects.create_user(**data)
        try:
            send_mail('email/create_user.tpl', data, settings.DEFAULT_FROM_EMAIL, [user.login])
        except:
            pass

        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()
            data = {
                'name': instance.name,
                'login':  instance.login,
                'password': validated_data['password']
            }
            try:
                send_mail('email/update_password.tpl', data, settings.DEFAULT_FROM_EMAIL, [instance.login])
            except:
                pass

        return instance

    def validate(self, data):
        if 'password' in data:
            validate_password(data['password'])

            if data.get('password_confirm') != data.get('password'):
                raise serializers.ValidationError({
                    'password_confirm':_('Поля пароля и подтверждение пароля должны совпадать')
                })
        return data


class RestoreAccessSerializer(serializers.Serializer):
    login = serializers.EmailField(max_length=128, allow_blank=False)

    def validate(self, data):
        if not ExtUser.objects.filter(login=data.get('login')):
            raise serializers.ValidationError({'login': _('Пользователь с таким почтовым ящиком не существует')})
        return data

    # Send token for authorization this user
    def save(self):
        to_email = self.validated_data['login']
        user = ExtUser.objects.get(login=to_email)
        token, _ = Token.objects.get_or_create(user=user)
        data = { 'name': user.name, 'token':  token.key }
        send_mail('email/restore_access.tpl', data, settings.DEFAULT_FROM_EMAIL, [to_email])

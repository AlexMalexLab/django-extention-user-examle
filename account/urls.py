from django.urls import path
from rest_framework import routers
from .views import Login, Registration, UserViewSet, Profile, RestoreAccess, oauth, auth_by_token

app_name = 'account'

router = routers.SimpleRouter()
router.register(r'api', UserViewSet)

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', Registration.as_view(), name='signup'),
    path('profile/', Profile.as_view(), name='profile'),
    path('restore/', RestoreAccess.as_view(), name='restore'),
    path('oauth/<mode>/', oauth, name='oauth'),
    path('auth_by_token/<token>/', auth_by_token, name='auth_by_token'),



]

urlpatterns += router.urls



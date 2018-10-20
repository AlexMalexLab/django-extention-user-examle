from django.conf import settings
from django.urls import reverse
from oauth2client.client import OAuth2WebServerFlow


def get_all_flows():
    return {mode: get_flow(mode) for mode, v in settings.ACCOUNT_OAUTH2.items()}


def get_flow(mode):
    arr = settings.ACCOUNT_OAUTH2[mode].copy()
    arr.update({'redirect_uri': settings.ACCOUNT_OAUTH2_REDIRECT_HOST + reverse('account:oauth', args=[mode])})
    return OAuth2WebServerFlow(**arr)

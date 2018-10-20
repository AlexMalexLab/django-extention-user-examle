# django-extention-user-examle
It's part of planengo.ru

Это django 2.0 приложение для создания расширенного пользователя вместо стандартного на основе встроенных в Django классов AbstractBaseUser и BaseUserManager.

Поле login является e-mail и используется для входа вместо username.
Специфический набор полей, поддержка входа через OAuth facebook и google.
Рассылка уведомлений на основе шаблонных писем.
Работа через API Django Rest Frameworks.

Подключение в файле settings.py

LOGIN_URL = 'account:login'
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'account.ExtUser'

в urls.py
urlpatterns += [...
    path('account/', include('account.urls', namespace='account')),
...]

Имеется потдержка OAuth авторизации для входа/создания пользователя по E-Mail
Для этого в файле settings.py вашего проекта надо прописать 
ACCOUNT_OAUTH2 = {
    'google': {
        "client_id": "YOUR-DATA.apps.googleusercontent.com",
        "client_secret": "YOUR-DATA",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "scope": ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
    },
    'facebook': {
        "client_id": "YOUR-DATA",
        "client_secret": "YOUR-DATA",
        "auth_uri": "https://www.facebook.com/dialog/oauth",
        "token_uri": "https://graph.facebook.com/oauth/access_token",
        "scope": 'email'
    }
}
ACCOUNT_OAUTH2_REDIRECT_HOST = 'https://YOUR-SITE.ru'

В шаблонах 
<a href="{{ oauth_url.facebook.step1_get_authorize_url }}" class="social__soc social__soc_fb"></a>
<a href="{{ oauth_url.google.step1_get_authorize_url }}" class="social__soc social__soc_gplus"></a>


Данный модель представлен для BackEnd.


--------
Как подключить FrontEnd
Без интеграции с основным шаблон файлов, другой статики по проекту, Vue.js, Webpack, Babel и доп. модулей ForntEnd часть в данном депозитарии представлена в качестве примеров. 

Если вас интересует как это работает через ForntEnd то, можете посмотреть на сайте 
https://planengo.ru/account/login/
https://planengo.ru/account/signup/


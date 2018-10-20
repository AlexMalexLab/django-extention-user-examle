{% extends "mail_templated/base.tpl" %}

{% block subject %}
Здравствуйте, {{ name }}. Восстановление доступа на Planengo.ru
{% endblock %}

{% block body %}
Мы получили запрос на восстановление доступа к Planengo.ru

Для входа на сайт воспользуйтесь специальной ссылкой:
http://planengo.ru/account/auth_by_token/{{ token }}

Ваш токен для входа в приложение:
{{ token }}

{% endblock %}

{% block html %}
Мы получили запрос на восстановление доступа к Planengo.ru<br/>
<br/>
Для входа на сайт воспользуйтесь специальной ссылкой:<br/>
<a href="http://planengo.ru/account/auth_by_token/{{ token }}">http://planengo.ru/account/auth_by_token/{{ token }}</a><br/>
<br/>
Ваш токен для входа в приложение:<br/>
{{ token }}<br/>
<br/>
{% endblock %}
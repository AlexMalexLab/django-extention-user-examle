{% extends "mail_templated/base.tpl" %}

{% block subject %}
Здравствуйте, {{ name }}. Регистрация на Planengo.ru
{% endblock %}

{% block body %}
Здравствуйте, {{ name }}.
Спасибо за регисрацию на Planengo.ru.

Ваши данные для входа:
Логин: {{ login }}
Пароль: {{ password }}

{% endblock %}

{% block html %}
Здравствуйте, {{ name }}.<br/>
Спасибо за регисрацию на Planengo.ru.<br/>
<br/>
Ваши данные для входа:<br/>
Логин: <b>{{ login }}</b><br/>
Пароль: <b>{{ password }}</b><br/>
<br/>
{% endblock %}
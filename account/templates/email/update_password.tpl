{% extends "mail_templated/base.tpl" %}

{% block subject %}
Здравствуйте, {{ name }}. Вы изменили данные для входа на Planengo.ru
{% endblock %}

{% block body %}
Вы изменили данные для входа на Planengo.ru

Ваши новые данные для входа:
Логин: {{ login }}
Пароль: {{ password }}

{% endblock %}

{% block html %}
Вы изменили данные для входа на Planengo.ru<br/>
<br/>
Ваши новые данные для входа:<br/>
Логин: <b>{{ login }}</b>
Пароль: <b>{{ password }}</b>

{% endblock %}
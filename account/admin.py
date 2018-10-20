from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import ExtUser

@admin.register(ExtUser)
class ExtUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Личная информация'), {'fields': ('name', 'birthday', 'country', 'city', 'interests')}),
        (_('Платежная информация'), {'fields': ('ya_purse', 'balance')}),

        (_('Права доступа'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'added')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('added', 'balance')

    list_display = ('id', 'login', 'name', 'balance', 'last_login', 'added')
    list_display_links = ['id', 'login', 'name']

    list_filter = ('is_active', 'groups')
    search_fields = ('login', 'name')
    ordering = ('added',)
    filter_horizontal = ()

#admin.site.register(ExtUser, ExtUserAdmin)
import os
from django.conf import settings
from django.contrib.auth.models import Group, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from image.service import resize


class ExtUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login, password, **fields):
        if not login:
            raise ValueError(_('Логин должен быть установлен'))
        login = self.model.normalize_username(self.normalize_email(login))
        user = self.model(login=login, **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, password=None, **fields):
        fields.setdefault('is_staff', False)
        fields.setdefault('is_superuser', False)
        fields.setdefault('name', login.split('@')[0])

        user = self._create_user(login, password, **fields)
        user.groups.add(Group.objects.get(name='User'))

        return user

    def create_superuser(self, login, password, **fields):
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)
        fields.setdefault('name', login.split('@')[0])

        if fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))

        return self._create_user(login, password, **fields)


class ExtUser(AbstractBaseUser, PermissionsMixin):

    login = models.EmailField(
        max_length=150,
        unique=True,
        error_messages={'unique': _("Пользователь с таким почтовым ящиком уже существует")},
        verbose_name=_('Логин (E-mail)'),
    )
    name = models.CharField(max_length=100, blank=False, verbose_name=_('Имя'))
    birthday = models.DateField(null=True, blank=True, verbose_name=_('День рождения'))
    country = models.CharField(max_length=100, blank=True, verbose_name=_('Страна'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('Город'))
    interests = models.TextField(blank=True, verbose_name=_('Интересы'))
    ya_purse = models.CharField(max_length=30, blank=True, verbose_name=_('Яндек.Кошелек'))
    avatar = models.ImageField(upload_to='avatar', blank=True, verbose_name=_('Аватар'))

    balance = models.FloatField(default=0, verbose_name=_('Баланс'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Персонал'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))
    added = models.DateTimeField(default=now, verbose_name=_('Добавлено'))

    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'login'
    EMAIL_FIELD = 'login'

    objects = ExtUserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def save(self, *args, **kwargs):
        if not self.name and self.login:
            self.name = self.login.split('@')[0]

        qs = ExtUser.objects.filter(pk=self.pk)
        is_new = False if self.pk and qs.exists() else True
        old_obj = None if is_new else qs.get()

        super().save(*args, **kwargs)

        size = 100
        if is_new:
            if self.avatar:
                full_name = os.path.join(settings.MEDIA_ROOT, self.avatar.name)
                resize(full_name, 's', size, replace=True)
        else:
            if self.avatar != old_obj.avatar:
                if self.avatar:
                    full_name = os.path.join(settings.MEDIA_ROOT, self.avatar.name)
                    resize(full_name, 's', size, replace=True)
                if old_obj.avatar:
                    old_full_name = os.path.join(settings.MEDIA_ROOT, old_obj.avatar.name)
                    if os.path.isfile(old_full_name):
                        os.remove(old_full_name)


from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import jwt
from .managers import UserManager
import datetime
import secrets


def generate_access_token(user, is_staff):
    access_token_payload = {
        'user_id': user.id,
        'is_staff': is_staff,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token


def generate_refresh_token(user, is_staff):
    refresh_token_payload = {
        'user_id': user.id,
        'is_staff': is_staff,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

    return refresh_token


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    login = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def status(self):
        return self.student


class Group(models.Model):
    class Meta:
        verbose_name = 'Группа учащегося'
        verbose_name_plural = 'Группа учащегося'
        unique_together = ('name', 'subgroup')

    name = models.CharField(max_length=30)
    subgroup = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.subgroup})' if self.subgroup else self.name


class Student(models.Model):
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студент'

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    is_headman = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Teacher(models.Model):
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватель'

    surname = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.surname} {self.first_name[0]}. {self.patronymic[0]}.'

from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import MEDIA_ROOT

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Телефон')
    city = models.CharField(max_length=30, verbose_name='Город')
    avatar = models.ImageField(upload_to=f'{MEDIA_ROOT}/users/', **NULLABLE, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['id']
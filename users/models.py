from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватарка', **NULLABLE)

    email = models.EmailField(unique=True, verbose_name='email')
    username = None

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.email})'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

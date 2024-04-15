from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, unique=True, verbose_name='Электронная почта')
    phone = models.CharField(max_length=35, verbose_name='phone number', null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name='country', null=True, blank=True)
    is_password_reset = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=8)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


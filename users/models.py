from django.contrib.auth.models import AbstractUser
from django.db import models

from blog.models import NULLABLE


class User(AbstractUser):
    """Модель пользователей"""
    username = None

    first_name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(unique=True, verbose_name='email')
    phone_number = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE, help_text='введите номер телефона')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', **NULLABLE, help_text='загрузите свой аватар')
    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активный')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email

    permissions = [
        ('can_view_user', 'Может просматривать пользователей'),
        ('can_block_user', 'Может блокировать пользователей')
    ]



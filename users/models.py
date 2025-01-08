from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Моель кастомного пользователя"""

    username = None

    email = models.EmailField(unique=True, verbose_name="Почта")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

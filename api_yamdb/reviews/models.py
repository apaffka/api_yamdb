from django.contrib.auth.models import AbstractUser
from django.db import models

# создаём последовательность для выбора роли пользователя
USER_ROLE_CHOICES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]


class User(AbstractUser):
    """Класс для пользовательской модели."""
    email = models.EmailField(
        'email address',
        blank=False,
        unique=True,
        max_length=254,
    )
    bio = models.TextField('bio', blank=True)
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default='user',
    )


class Categories(models.Model):
    pass


class Genres(models.Model):
    pass


class Titles(models.Model):
    pass


class Review(models.Model):
    pass


class Comments(models.Model):
    pass


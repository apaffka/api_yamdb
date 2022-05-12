from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):
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
    name = models.TextField(
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
    )


class Genres(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=25,
    )
    slug = models.SlugField(
        max_length=25,
    )


class Titles(models.Model):
    name = models.CharField(
        blank=False,
        max_length=150,
    )
    year = models.IntegerField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT,
        related_name='category',
    )

# class Group(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()
#
#     def __str__(self):
#         return self.title
#
#
# class Post(models.Model):
#     text = models.TextField()
#     pub_date = models.DateTimeField(
#         'Дата публикации', auto_now_add=True
#     )
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='posts'
#     )
#     image = models.ImageField(
#         upload_to='posts/', null=True, blank=True
#     )
#     group = models.ForeignKey(
#         Group, on_delete=models.CASCADE,
#         related_name='posts', blank=True, null=True
#     )
#
#     def __str__(self):
#         return self.text
#
#
# class Comment(models.Model):
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='comments'
#     )
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='comments'
#     )
#     text = models.TextField()
#     created = models.DateTimeField(
#         'Дата добавления', auto_now_add=True, db_index=True
#     )

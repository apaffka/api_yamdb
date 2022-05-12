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
        max_length=50,
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
    genres = models.ManyToManyField(Genres, through='GenreTitle')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE
    )
    genre_id = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE
    )


class Reviews(models.Model):
    title_id = models.OneToOneField(
        Titles,
        verbose_name='titles',
        on_delete=models.PROTECT,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )


class Comments(models.Model):
    review_id = models.OneToOneField(
        Reviews,
        verbose_name='reviews',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

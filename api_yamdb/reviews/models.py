from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
    code = models.CharField(
        max_length=50,
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug

class Genres(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=25,
    )
    slug = models.SlugField(
        max_length=25,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Titles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        blank=False,
        max_length=150,
    )
    year = models.IntegerField()
    description = models.TextField(
        'description',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT,
        related_name='category',
    )
    genres = models.ManyToManyField(
        Genres,
        through='GenreTitle'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE
    )


class Reviews(models.Model):
     id = models.AutoField(primary_key=True)
     title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
     text = models.TextField()
     author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
     score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
     pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

     class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name='unique_review_for_title'
            ),
        ]

     def __str__(self):
         return self.text


class Comments(models.Model):
     id = models.AutoField(primary_key=True)
     review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Дата публикации'
    )
     text = models.TextField()
     author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
     pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )


     class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

     def __str__(self):
        return self.text[:15]

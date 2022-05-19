from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg

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
    code = models.TextField(
        max_length=50,
        blank=False,
        unique=True,
    )
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['bio', 'role', 'code','email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Categories(models.Model):
    name = models.TextField(
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=25,
    )
    slug = models.SlugField(
        max_length=25,
        unique=True,
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
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
    title = models.ForeignKey(
        Titles,
        verbose_name='reviews',
        on_delete=models.PROTECT,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    # На одно произведение пользователь может оставить только один отзыв.
    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return self.text





class Comments(models.Model):
    review = models.ForeignKey(
        Reviews,
        verbose_name='comments',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text
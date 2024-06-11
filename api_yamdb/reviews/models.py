from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=6,
        blank=True,
        null=True)
    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True)
    last_name = models.CharField(
        max_length=30,
        blank=True,
        null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Review(models.Model):
    title = models.IntegerField()  # Заглушка для ForeingKey(Title, )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rewiews'
    )
    score = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    rewiew = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Category(models.Model):
    """Model of category."""
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное имя категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name  # TODO: fix this title


class Genre(models.Model):
    """Model of genre."""
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное имя жанра')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Model of title."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год создания произведения')
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

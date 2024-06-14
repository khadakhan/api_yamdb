from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import lte_current_year_validator
from api_yamdb import settings

SCORES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=6,
        default=0,
        blank=True)
    first_name = models.CharField(
        max_length=30,
        blank=True)
    last_name = models.CharField(
        max_length=30,
        blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        return self.email


class Category(models.Model):
    """Model of category."""
    name = models.CharField(
        max_length=settings.MAX_CHAR_NAME,
        verbose_name='Название категории')
    slug = models.SlugField(
        max_length=settings.MAX_CHAR_SLUG,
        unique=True,
        verbose_name='Уникальное имя категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Model of genre."""
    name = models.CharField(
        max_length=settings.MAX_CHAR_NAME,
        verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=settings.MAX_CHAR_SLUG,
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
        max_length=settings.MAX_CHAR_NAME,
        verbose_name='Название произведения')
    year = models.SmallIntegerField(
        verbose_name='Год создания произведения', validators=(
            lte_current_year_validator,))
    description = models.TextField(
        default='',
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


class Review(models.Model):
    """Review model."""
    title = models.ForeignKey(
        Title,
        # При удалении объекта произведения Title должны удаляться все
        # отзывы к этому произведению и комментарии к ним.
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Идентификатор произведения'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name='Оценка произведения'
    )

    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(models.Model):
    """Comment model."""
    review = models.ForeignKey(
        Review,
        # При удалении объекта отзыва Review должны быть удалены
        # все комментарии к этому отзыву.
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Идентификатор отзыва'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

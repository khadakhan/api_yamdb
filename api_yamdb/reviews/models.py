from django.contrib.auth import get_user_model
from django.db import models


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
        return self.title


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
        return self.title

from datetime import datetime

from django.contrib.admin.filters import ValidationError
from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category viewset."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre viewset."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for title viewset."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('name', 'year', 'description', 'ganre', 'category')
        model = Title

    def validate_year(self, creation_year):
        if creation_year > datetime.now().year:
            raise ValidationError(
                'You cannot add a title that has not yet been published.')
        return creation_year

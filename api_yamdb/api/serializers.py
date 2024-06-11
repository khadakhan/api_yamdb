from datetime import datetime

from django.contrib.admin.filters import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from reviews.models import Category, Genre, Title


class BaseConnectorToSlug:
    """Provide method to change incoming data while serialize."""

    def to_internal_value(self, slug):
        try:
            object_with_slug = self.Meta.model.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f'Incorrect slug {slug}')
        return object_with_slug


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


class GenreAnotherSerializer(BaseConnectorToSlug, GenreSerializer):
    """Change input value Genre model while serialize."""


class CategoryAnotherSerializer(BaseConnectorToSlug, CategorySerializer):
    """Change input value Category model while serialize."""


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for title viewset."""

    genre = GenreAnotherSerializer(many=True)
    category = CategoryAnotherSerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, creation_year):
        if creation_year > datetime.now().year:
            raise ValidationError(
                'You cannot add a title that has not yet been published.')
        return creation_year

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data)

        title.category = category
        for genre in genres:
            title.genre.add(genre)
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        if 'genre' in validated_data:
            instance.genre.clear()
            for genre in validated_data['genre']:
                instance.genre.add(genre)
        return instance

import random
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, SCORES
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class BaseConnectorToSlug:
    """Provide method to change incoming data while serialize."""

    def to_internal_value(self, slug):
        try:
            object_with_slug = self.Meta.model.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f'Incorrect slug {slug}')
        return object_with_slug


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Имя пользователя 'me' недоступно")
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if not username or not confirmation_code:
            raise ValidationError(
                'Имя пользователя и код подтверждения обязательны.')
        user = User.objects.filter(
            username=username, confirmation_code=confirmation_code).first()
        if user is None:
            raise ValidationError('Неправильный код или имя пользователя.')
        data['user'] = user
        return data


class TitleIdDefault:
    """
    Class for extract title_id.
    """
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].data.get('title_id')


class ReviewSerializer(ModelSerializer):
    """Review serializer."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.ChoiceField(choices=SCORES)
    title_id = serializers.HiddenField(default=TitleIdDefault())

    class Meta:
        fields = ('text',
                  'title_id',
                  'author',
                  'score',
                  'pub_date')
        model = Review
        # На одно произведение пользователь может оставить только один отзыв.
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title_id', 'author'),
                message=("Пользователь может лишь один раз оставить отзыв"
                         "к произведению!")
            )
        ]


class CommentSerializer(ModelSerializer):
    """Comment serializer."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('text',
                  'author',
                  'pub_date')
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(ModelSerializer):
    """Serializer for category viewset."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(ModelSerializer):
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
    rating = serializers.SerializerMethodField()
    category = CategoryAnotherSerializer()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category')
        model = Title

    def get_rating(self, title):
        return title.reviews.all().aggregate(
            rating=Cast(Avg('score'), output_field=IntegerField()))['rating']

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

from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, SCORES

User = get_user_model()


class ConnectorToSlug(serializers.RelatedField):
    """Provide methods to change incoming data while serialize."""

    def __init__(self, *args, base_serializer, **kwargs):
        self.base_serializer = base_serializer
        super().__init__(*args, **kwargs)

    def get_model(self):
        return self.base_serializer.Meta.model

    def to_internal_value(self, slug):
        try:
            object_with_slug = self.get_model().objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f'Incorrect slug {slug}')
        return object_with_slug

    def get_queryset(self):
        return self.get_model.object.all()

    def to_representation(self, instance):
        return self.base_serializer(instance).data


class UserSerializer(ModelSerializer):
    """User serializer."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Имя пользователя 'me' недоступно")
        return value

    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)


class TokenSerializer(serializers.Serializer):
    """Token serializer."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(
            username=data.get('username'),
            confirmation_code=data.get('confirmation_code')).first()
        if user is None:
            raise ValidationError('Неправильный код или имя пользователя.')
        data['user'] = user
        return data


class ReviewSerializer(ModelSerializer):
    """Review serializer."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.ChoiceField(choices=SCORES)
    title = serializers.HiddenField(
        default=serializers.PrimaryKeyRelatedField(
            queryset=Title.objects.all(),
        )
    )

    def validate_title(self, value):
        # Кто бы мог подумать???
        title = self.context['view'].kwargs['title_id']
        return get_object_or_404(Title, pk=title)

    class Meta:
        fields = ('text',
                  'id',
                  'title',
                  'author',
                  'score',
                  'pub_date')
        model = Review
        # На одно произведение пользователь может оставить только один отзыв.
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message=("Пользователь может оставить только один отзыв"
                         " к произведению!")
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
                  'pub_date',
                  'id')
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


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer for read title viewset."""

    genre = GenreSerializer()
    category = CategorySerializer()


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for title viewset."""

    genre = ConnectorToSlug(base_serializer=GenreSerializer, many=True)
    rating = serializers.IntegerField(read_only=True)
    category = ConnectorToSlug(base_serializer=CategorySerializer)

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

    def validate_genre(self, genre):
        if not genre:
            raise ValidationError('Title must have genre.')
        return genre

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data)

        title.category = category
        for genre in genres:
            title.genre.add(genre)
        title.save()
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
        instance.save()
        return instance

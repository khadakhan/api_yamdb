from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UnicodeUsernameValidator
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from reviews.validators import validate_username_me
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(ModelSerializer):
    """User serializer."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)


class CodeSerializer(serializers.Serializer):
    """Code serializer."""
    username = serializers.CharField(
        max_length=settings.MAX_NAME_LENGTH,
        validators=(validate_username_me, UnicodeUsernameValidator()))
    email = serializers.EmailField(
        max_length=settings.MAX_EMAIL_LENGTH)

    def validate(self, data):
        email_user = User.objects.filter(
            email=data.get('email')).first()
        username_user = User.objects.filter(
            username=data.get('username')).first()
        if email_user != username_user:
            error_msg = {}
            if not email_user:
                error_msg['username'] = ('Пользователь с таким '
                                         'username уже существует.')
            if not username_user:
                error_msg['email'] = ('Пользователь с таким '
                                      'email уже существует.')
            raise ValidationError(error_msg)
        return data


class TokenSerializer(serializers.Serializer):
    """Token serializer."""
    username = serializers.CharField(
        max_length=settings.MAX_NAME_LENGTH, validators=(
            validate_username_me, UnicodeUsernameValidator))
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(
            User, username=data.get('username'))
        if not default_token_generator.check_token(
                user, data.get('confirmation_code')):
            raise ValidationError(
                'Неправильный код или имя пользователя.')
        return data


class ReviewSerializer(ModelSerializer):
    """Review serializer."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        curr_author = self.context['request'].user
        if (not self.context['request'].method == 'PATCH') and (
            Review.objects.select_related('title').filter(
                author=curr_author,
                title__id=title_id
            ).exists()
        ):
            raise ValidationError(
                'Пользователь может оставить только один отзыв'
                ' к произведению!')
        return data

    class Meta:
        fields = ('text',
                  'id',
                  'author',
                  'score',
                  'pub_date')
        model = Review


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
    """Serializer for category ViewSet."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(ModelSerializer):
    """Serializer for genre ViewSet."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(ModelSerializer):
    """Serializer for read title ViewSet."""

    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True, allow_null=True)
    category = CategorySerializer()

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


class TitleWriteSerializer(ModelSerializer):
    """Serializer for write to title ViewSet."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = (
            'name',
            'year',
            'description',
            'genre',
            'category')
        model = Title

    def to_representation(self, title):
        return TitleReadSerializer(title).data

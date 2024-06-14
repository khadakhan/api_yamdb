from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueTogetherValidator

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


class TokenSerializer(serializers.Serializer):
    """Token serializer."""
    username = serializers.CharField(
        max_length=settings.MAX_NAME_LENGTH,
        validators=[User.validate_username])
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

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        curr_author = self.context['request'].user
        for review in title.reviews.all():
            if review.author == curr_author:
                raise serializers.ValidationError(
                    "Пользователь может оставить только один отзыв"
                    " к произведению!"
                )

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


class TitleWriteSerializer(serializers.ModelSerializer):
    """Serializer for write to title viewset."""

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

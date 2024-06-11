import random
from datetime import datetime

from django.contrib.admin.filters import ValidationError
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Category, Comment, Genre, Review, Title

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
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Имя пользователя 'me' недоступно")
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return user
        confirmation_code = f'{random.randint(100000, 999999):06}'
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения - {confirmation_code}',
            'from@example.com',
            [user.email],
            fail_silently=False
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class ReviewSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('rewiew',)


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

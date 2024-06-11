import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, SCORES

User = get_user_model()


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
    """Review serializer."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.ChoiceField(choices=SCORES)

    class Meta:
        fields = ('text',
                  'author',
                  'score',
                  'pub_date')
        model = Review
        # На одно произведение пользователь может оставить только один отзыв.
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
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

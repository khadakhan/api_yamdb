import random

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer, ValidationError
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
        user, created = User.objects.get_or_create(**validated_data)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return user
        if not created:
            user.save()
        code = f'{random.randint(100000, 999999):06}'
        user.confirmation_code = code
        user.save()
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения - {code}',
            'from@example.com',
            [user.email],
            fail_silently=False)
        return user


class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        if not username or not confirmation_code:
            raise ValidationError(
                'Username and код подтверждения обязательны.')
        user = User.objects.filter(
            username=username, confirmation_code=confirmation_code).first()
        if not user:
            raise ValidationError(
                'Неправильный username или код подтверждения.')
        return {'token': str(RefreshToken.for_user(user))}

# # Это вычисляемое на лету поле rating для сериалайзера Title.
# rating = serializers.SerializerMethodField()

# def get_rating(self, obj):
#     rating = None
#     reviews = obj.reviews.all()
#     for review in reviews:
#         if review.score is not None:
#             rating += review.score
#     return rating / reviews.count()


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

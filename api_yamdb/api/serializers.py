import random

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Category, Comment, Genre, Review

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

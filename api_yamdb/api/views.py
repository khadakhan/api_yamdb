import random
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import filters, mixins, viewsets, status
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAdminUser)
from rest_framework.response import Response
from rest_framework.decorators import action
from reviews.models import Category, Genre, Review
from .serializers import (
    CategorySerializer, GenreSerializer, CommentSerializer,
    MyTokenObtainPairSerializer, UserSerializer,
    ReviewSerializer, TokenConfirmationSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permissions = {
        'default': [IsAdminUser],
        'create': [AllowAny],
        'signup': [AllowAny],
        'token': [AllowAny],
        'me': [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return (
                permission() for permission in
                self.permissions[self.action]
            )
        except KeyError:
            return (
                permission() for permission in
                self.permissions['default']
            )

    @action(detail=False,
            methods=['post'],
            permission_classes=[AllowAny])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = f'{random.randint(100000, 999999):06}'
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения - {confirmation_code}',
            'from@example.com',
            [user.email],
            fail_silently=False)
        return Response(
            data={'username': user.username, 'email': user.email},
            status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['post'],
            permission_classes=[AllowAny])
    def token(self, request):
        serializer = TokenConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        try:
            user = User.objects.get(
                username=username,
                confirmation_code=confirmation_code)
        except User.DoesNotExist:
            return Response(
                data={'detail': 'Неверно веден username или код'},
                status=status.HTTP_400_BAD_REQUEST)
        user.confirmation_code = None
        user.save()
        token_serializer = MyTokenObtainPairSerializer(
            data={'username': username, 'password': user.password})
        token_serializer.is_valid(raise_exception=True)
        return Response(
            token_serializer.validated_data,
            status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(post=self.get_review(), author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BaseCreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    """Base class to provide create, list, destroy acts."""


class CategoryViewSet(BaseCreateListDestroyViewSet):
    """ViewSet for category."""

    queryset = Category.objects.all()
    # TODO add permission class
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(BaseCreateListDestroyViewSet):
    """ViewSet for genre."""

    queryset = Genre.objects.all()
    # TODO add permission class
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

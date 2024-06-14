import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED)
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .permissions import (
    IsAdmin, ReadOnly, AuthorModeratorAdminOrReadOnly)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    ReviewSerializer,
    UserSerializer)
from .viewsets import BaseCreateListDestroyViewSet

User = get_user_model()


def generate_and_send_code(user):
    token = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения - {token}',
        from_email=settings.FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user flows."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    allowed_methods = ('get', 'post', 'patch',)
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        return self.partial_update(request)


class AuthViewSet(ViewSet):
    """ViewSet for authentication and token."""

    @action(detail=False, methods=['post'])
    def signup(self, request):
        username = request.data.get('username')
        user = User.objects.filter(
            email=request.data.get('email')).first()
        if not user or user.username != username:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        generate_and_send_code(user)
        return Response(
            data={'username': user.username, 'email': user.email},
            status=HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def token(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.data.get('username'))
        return Response(
            data={'token': str(AccessToken.for_user(user))},
            status=HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for comments."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get(
            'review_id'), title=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset for reviews."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)





class CategoryViewSet(BaseCreateListDestroyViewSet):
    """ViewSet for category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(BaseCreateListDestroyViewSet):
    """ViewSet for genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet for title."""

    queryset = Title.objects.prefetch_related('genre').select_related(
        'category').annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdmin | ReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

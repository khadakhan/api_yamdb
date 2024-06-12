import random
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from reviews.models import Category, Genre, Review, Title
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action, throttle_classes
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

from .filters import TitleFilter
from .permissions import IsAdmin, ReadOnly, AuthorOrReadOnly
from .throttling import TwoRequestsPerUserThrottle
from .permissions import AuthorOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    TokenSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer)

User = get_user_model()


def send_code(user):
    user.confirmation_code = f'{random.randint(0, 999999):06}'
    user.save()
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения - {user.confirmation_code}',
        from_email='from@example.com',
        recipient_list=[user.email],
        fail_silently=False)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('role',)
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return [IsAdmin()]

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        return self.partial_update(request)


class AuthViewSet(ViewSet):

    @action(detail=False, methods=['post'])
    def signup(self, request):
        username = request.data.get('username')
        existing_user = User.objects.filter(
            email=request.data.get('email')).first()
        if existing_user and existing_user.username == username:
            send_code(existing_user)
            return Response(
                data={'message': 'Новый код отправлен на почту'},
                status=HTTP_200_OK)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_code(user)
            return Response(
                data={'username': user.username, 'email': user.email},
                status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def token(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response(
                data={'token': str(RefreshToken.for_user(user).access_token)},
                status=HTTP_200_OK)
        username = request.data.get('username')
        if username and not User.objects.filter(username=username).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for comments."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review(self):
        return get_object_or_404(self.get_title().reviews.all(),
                                 id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review_id=self.get_review(), author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset for reviews."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title_id=self.get_title(), author=self.request.user)


class BaseCreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    """Base class to provide create, list, destroy acts."""


class CategoryViewSet(BaseCreateListDestroyViewSet):
    """ViewSet for category."""

    queryset = Category.objects.all()
    permission_classes = (IsAdmin | ReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(BaseCreateListDestroyViewSet):
    """ViewSet for genre."""

    queryset = Genre.objects.all()
    permission_classes = (IsAdmin | ReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet for title."""

    queryset = Title.objects.prefetch_related(
        'genre').select_related('category')
    permission_classes = (IsAdmin | ReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

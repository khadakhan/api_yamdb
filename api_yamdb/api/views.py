from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Genre, Review

from .serializers import (
    CategorySerializer, GenreSerializer, CommentSerializer,
    MyTokenObtainPairSerializer, UserSerializer, ReviewSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


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

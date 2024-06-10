from rest_framework import filters, viewsets, mixins

from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre


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

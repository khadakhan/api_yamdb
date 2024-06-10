from rest_framework import viewsets, mixins

from api.serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """ViewSet for category."""

    queryset = Category.objects.all()
    # TODO add permission class
    serializer_class = CategorySerializer
    lookup_field = 'slug'

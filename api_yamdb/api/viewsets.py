from rest_framework import filters, mixins, viewsets
from .permissions import IsAdmin, ReadOnly


class BaseCreateListDestroyViewSet(mixins.CreateModelMixin,
                                   mixins.ListModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    """Base class to provide create, list, destroy acts."""

    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

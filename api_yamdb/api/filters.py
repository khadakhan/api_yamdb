from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__slug',
        method='filter_category')
    genre = filters.CharFilter(
        field_name='genre__slug',
        method='filter_genre')

    class Meta:
        model = Title
        fields = ('name', 'year')

    def filter_category(self, queryset, name, category):
        return queryset.filter(
            category__slug__contains=category)

    def filter_genre(self, queryset, name, genre):
        return queryset.filter(
            genre__slug__contains=genre)

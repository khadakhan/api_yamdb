from rest_framework import serializers 

from reviews.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category viewset."""

    class Meta:
        fields = ('name', 'slug')
        model = Category

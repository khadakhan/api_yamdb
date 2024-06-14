from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .viewsets import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    AuthViewSet,
    CommentViewSet,
    ReviewViewSet)

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('auth', AuthViewSet, basename='auth')
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>.+?)/reviews',
                   ReviewViewSet,
                   basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>.+?)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]

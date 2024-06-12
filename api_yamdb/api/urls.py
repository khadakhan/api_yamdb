from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    AuthViewSet,
    CommentViewSet,
    ReviewViewSet)

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet)
v1_router.register(r'titles/(?P<title_id>.+?)/reviews',
                   ReviewViewSet,
                   basename='reviews')
v1_router.register(r'titles/(?P<title_id>.+?)/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/',
         AuthViewSet.as_view({'post': 'token'}),
         name='token_obtain_pair'),
    path('v1/auth/signup/',
         AuthViewSet.as_view({'post': 'signup'}),
         name='signup'),
    path('v1/users/me/',
         UserViewSet.as_view({'get': 'me', 'patch': 'me'}),
         name='user_profile'),
]

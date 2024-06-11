from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet,
                    GenreViewSet,
                    UserViewSet,
                    CommentViewSet,
                    ReviewViewSet)

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(r'titles/(?P<title_id>.+?)/reviews',
                   ReviewViewSet,
                   basename='reviews')
v1_router.register(r'titles/(?P<title_id>.+?)/reviews/{review_id}/comments',
                   CommentViewSet,
                   basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', UserViewSet.as_view({'post': 'signup'}), name='signup'),
    path('v1/auth/token/', UserViewSet.as_view({'post': 'token'}), name='token_obtain_pair'),
    path('v1/users/me/', UserViewSet.as_view({'get': 'me', 'patch': 'me'}), name='user_profile'),
]

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet)
# ...

url_v1 = [
    # path('auth', ...)
    path('', include(v1_router.urls)),
]

urlpatterns = [
    path('v1/', include(url_v1)),
]

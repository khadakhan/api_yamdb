from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CategoryViewSet

app_name = 'api'

router = SimpleRouter()
router.register('categories', CategoryViewSet) 
# ...

url_v1 = [
    # path('auth', ...)
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(url_v1)),
]

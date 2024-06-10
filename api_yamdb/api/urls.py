from django.urls import include, path
from rest_framework.routers import SimpleRouter

app_name = 'api'

router = SimpleRouter()
# ...

url_v1 = [
    # path('auth', ...)
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(url_v1)),
]

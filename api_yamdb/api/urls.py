from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, SignUpView, MyTokenObtainPairView

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')

url_v1 = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include(url_v1)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

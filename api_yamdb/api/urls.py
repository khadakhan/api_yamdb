from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, SignUpView, MyTokenObtainPairView

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

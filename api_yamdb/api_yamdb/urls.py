from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Python API на Django REST Framework",
      default_version='v1',
      description="Документация для проекта DRF API",
      contact=openapi.Contact(email="from@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

urlpatterns += [
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'),
]

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import UserViewSet


app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

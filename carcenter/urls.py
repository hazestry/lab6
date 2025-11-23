from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from api.views import ClientViewSet, CarViewSet, OrderViewSet

# Настройка роутера для API
router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'cars', CarViewSet, basename='car')
router.register(r'orders', OrderViewSet, basename='order')

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Car Center API",
        default_version='v1',
        description="API для автомобильного центра (продажа, ремонт авто)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@carcenter.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Swagger Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
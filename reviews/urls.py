from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reviews import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    path('api/auth/register/', views.RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('swagger/', views.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', views.schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

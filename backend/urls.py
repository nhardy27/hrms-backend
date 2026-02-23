from django.contrib import admin
from django.urls import path, include

# Main URL configuration for the project
urlpatterns = [
    # Admin panel (commented out for security)
    # path('admin/', admin.site.urls),
    
    # API endpoints (v1)
    path('api/v1/',include('api.urls')),
    
    # Authentication endpoints (login, token refresh, etc.)
    path('auth/',include('security.urls')),
    
    # DRF browsable API login (commented out)
    # path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
]

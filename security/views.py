from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import CustomTokenRefreshSerializer

class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom token refresh view.
    Extends the default JWT token refresh to use custom serializer.
    Endpoint: POST /auth/token/refresh/
    """
    serializer_class = CustomTokenRefreshSerializer
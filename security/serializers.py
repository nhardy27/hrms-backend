
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom serializer for JWT token refresh.
    Returns both new access token and refresh token.
    """
    def validate(self, attrs):
        # Create new refresh token from the provided token
        refresh = RefreshToken(attrs['refresh'])

        # Return both refresh and access tokens
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data
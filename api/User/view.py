from django.contrib.auth.models import User
from api.User.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from api.permissions import CustomPermission

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [CustomPermission]

    def get_queryset(self):
        user = self.request.user

        # agar superuser hai → sab users dikhao
        if user.is_superuser:
            return User.objects.all()

        # warna sirf logged-in user ka data
        return User.objects.filter(id=user.id)

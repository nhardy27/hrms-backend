from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .model import Designation
from .serializer import DesignationSerializer

class DesignationViewSet(ModelViewSet):
    serializer_class = DesignationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Designation.objects.select_related('department').all().order_by('-created_at')

        if hasattr(user, 'userprofile') and user.userprofile.department:
            return Designation.objects.filter(department=user.userprofile.department)

        return Designation.objects.none()

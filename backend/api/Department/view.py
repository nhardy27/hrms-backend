from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .model import Department
from .serializer import DepartmentSerializer


class DepartmentViewSet(ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # 🔑 Superuser → sab departments
        if user.is_superuser:
            return Department.objects.all().order_by("-created_at")

        # 👤 Normal user → sirf uska department
        if hasattr(user, "userprofile") and user.userprofile.department:
            return Department.objects.filter(
                id=user.userprofile.department.id
            )

        # ❌ Agar department hi assign nahi
        return Department.objects.none()

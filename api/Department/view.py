from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .model import Department
from .serializer import DepartmentSerializer


class DepartmentViewSet(ModelViewSet):
    """
    ViewSet for Department management.
    Handles CRUD operations for departments with role-based filtering.
    """
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter departments based on user role:
        - Superuser: can see all departments
        - Normal user: can only see their assigned department
        """
        user = self.request.user

        # Superuser can see all departments
        if user.is_superuser:
            return Department.objects.all().order_by("-created_at")

        # Normal user can only see their department
        if hasattr(user, "userprofile") and user.userprofile.department:
            return Department.objects.filter(
                id=user.userprofile.department.id
            )

        # If no department assigned, return empty queryset
        return Department.objects.none()

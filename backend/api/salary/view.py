from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .model import Salary
from .serializer import SalarySerializer


class SalaryViewSet(viewsets.ModelViewSet):
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Salary.objects.filter(deleted_at__isnull=True)

        return Salary.objects.filter(
            attendance__user=user,
            deleted_at__isnull=True
        )

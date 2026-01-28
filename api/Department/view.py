from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .model import Department
from .serializer import DepartmentSerializer

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all().order_by("-created_at")
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

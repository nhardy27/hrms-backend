from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .model import Employee
from .serializer import  EmployeeAddressSerializer





class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeAddressSerializer
    permission_classes = [IsAuthenticated]

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .model import AttendanceStatus
from .serializer import AttendanceStatusSerializer


class AttendanceStatusViewSet(viewsets.ModelViewSet):
    
    serializer_class = AttendanceStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AttendanceStatus.objects.filter(deleted_at__isnull=True)

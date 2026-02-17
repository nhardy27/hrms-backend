from rest_framework import viewsets
from .model import AttendanceStatus
from .serializer import AttendanceStatusSerializer

class AttendanceStatusViewSet(viewsets.ModelViewSet):
    queryset = AttendanceStatus.objects.filter(deleted_at__isnull=True)
    serializer_class = AttendanceStatusSerializer

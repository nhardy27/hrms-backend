from rest_framework import viewsets, status
from rest_framework.response import Response
from .model import AttendanceStatus
from .serializer import AttendanceStatusSerializer


class AttendanceStatusViewSet(viewsets.ModelViewSet):
    queryset = AttendanceStatus.objects.filter(deleted_at__isnull=True)
    serializer_class = AttendanceStatusSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = instance.updated_at
        instance.save()
        return Response(
            {"message": "Attendance status deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

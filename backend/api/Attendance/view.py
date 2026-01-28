from rest_framework import viewsets
from api.Attendance.model import Attendance
from api.Attendance.serializer import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = Attendance.objects.filter(deleted_at__isnull=True)

        employee_id = self.request.query_params.get("employee")
        date = self.request.query_params.get("date")

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        if date:
            queryset = queryset.filter(date=date)

        return queryset

from rest_framework import serializers
from api.Attendance.model import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source="employee.first_name",
        read_only=True
    )
    status_name = serializers.CharField(
        source="attendance_status.name",
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "employee",
            "employee_name",
            "date",
            "attendance_status",
            "status_name",
            "check_in",
            "check_out",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        employee = data.get("employee")
        date = data.get("date")

        if Attendance.objects.filter(
            employee=employee,
            date=date,
            deleted_at__isnull=True
        ).exists():
            raise serializers.ValidationError(
                "Attendance already marked for this employee on this date."
            )

        return data

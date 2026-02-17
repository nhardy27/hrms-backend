from rest_framework import serializers
from .model import Attendance
from api.UserProfile.model import UserProfile


class AttendanceSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username", read_only=True)
    emp_code = serializers.SerializerMethodField(read_only=True)

    status_name = serializers.CharField(
        source="attendance_status.get_status_display",
        read_only=True
    )

    total_hours = serializers.DurationField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id",
            "user",
            "username",
            "date",
            "attendance_status",
            "status_name",
            "check_in",
            "check_out",
            "total_hours",
            "emp_code",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = (
            "id",
            "emp_code",
            "total_hours",
            "created_at",
            "updated_at",
        )

    def get_emp_code(self, obj):
        try:
            return obj.user.userprofile.emp_code
        except UserProfile.DoesNotExist:
            return None

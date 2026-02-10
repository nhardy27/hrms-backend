from rest_framework import serializers
from .model import Attendance
from api.UserProfile.model import UserProfile


class AttendanceSerializer(serializers.ModelSerializer):
    # 🔹 Extra readable fields
    username = serializers.CharField(source="user.username", read_only=True)
    emp_code = serializers.SerializerMethodField(read_only=True)
    status_name = serializers.SerializerMethodField(read_only=True)
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

    def get_status_name(self, obj):
        status = obj.attendance_status
        if getattr(status, "present", False):
            return "Present"
        elif getattr(status, "halfday", False):
            return "Half Day"
        return "Absent"

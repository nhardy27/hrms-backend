from rest_framework import serializers
from .model import AttendanceStatus


class AttendanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceStatus
        fields = [
            "id",
            "present",
            "absent",
            "halfday",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

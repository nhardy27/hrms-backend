from rest_framework import serializers
from .model import Leave


class LeaveSerializer(serializers.ModelSerializer):
    # readable fields
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Leave
        fields = [
            "id",
            "user",
            "username",
            "from_date",
            "to_date",
            "reason",
            "status",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

from rest_framework import serializers
from .model import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

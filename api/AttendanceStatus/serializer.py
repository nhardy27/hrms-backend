from rest_framework import serializers
from .model import AttendanceStatus

class AttendanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceStatus
        fields = "__all__"

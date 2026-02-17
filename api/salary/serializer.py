from rest_framework import serializers
from .model import Salary


class SalarySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Salary
        fields = '__all__'

    def get_user(self, obj):
        attendance = getattr(obj, 'attendance', None)

        if attendance and attendance.user:
            user = attendance.user
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }

        return {
            "id": None,
            "username": "",
            "email": ""
        }

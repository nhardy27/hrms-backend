from rest_framework import serializers
from api.UserProfile.model import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'emp_code',
            'username',
            'email',
            'first_name',
            'last_name',
            'address',
            'bank_name',
            'bank_account_number',
            'ifsc_code',
            'department',
            'department_name',
            'contact_no',
            'designation',
            'date_of_joining',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['emp_code', 'created_at', 'updated_at', 'username', 'email']

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

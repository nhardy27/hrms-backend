from rest_framework import serializers
from .model import Employee
from api.Department.model import Department 


class EmployeeAddressSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    class Meta:
        model = Employee
        fields = [
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'email',
            'department',
            'department_name',
            'phone',
            'designation',
            'date_of_joining',
            'status',
            'created_at',
            'updated_at'
        ]

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

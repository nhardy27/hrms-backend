from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from api.UserProfile.model import UserProfile
from api.Department.model import Department
from api.Attendance.model import Attendance

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        required=False
    )
    contact_no = serializers.CharField(max_length=15, required=False)
    department = serializers.UUIDField(required=False)
    designation = serializers.CharField(max_length=30, required=False)
    date_of_joining = serializers.DateField(required=False)
    address = serializers.CharField(required=False)
    bank_name = serializers.CharField(max_length=100, required=False)
    bank_account_number = serializers.CharField(max_length=30, required=False)
    ifsc_code = serializers.CharField(max_length=20, required=False)
    department_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups', 'is_staff', 'is_active', 'contact_no', 'department', 'department_name', 'designation', 'date_of_joining', 'address', 'bank_name', 'bank_account_number', 'ifsc_code']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        try:
            profile = instance.userprofile
            representation['emp_code'] = profile.emp_code
            representation['contact_no'] = profile.contact_no
            representation['department'] = str(profile.department_id) if profile.department_id else None
            representation['department_name'] = self.get_department_name(instance)
            representation['designation'] = profile.designation
            representation['date_of_joining'] = profile.date_of_joining
            representation['address'] = profile.address
            representation['bank_name'] = profile.bank_name
            representation['bank_account_number'] = profile.bank_account_number
            representation['ifsc_code'] = profile.ifsc_code
        except UserProfile.DoesNotExist:
            representation['emp_code'] = None
            representation['contact_no'] = None
            representation['department'] = None
            representation['department_name'] = None
            representation['designation'] = None
            representation['date_of_joining'] = None
            representation['address'] = None
            representation['bank_name'] = None
            representation['bank_account_number'] = None
            representation['ifsc_code'] = None

        return representation

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        profile_data = {
            'contact_no': validated_data.pop('contact_no', None),
            'department_id': validated_data.pop('department', None),
            'designation': validated_data.pop('designation', None),
            'date_of_joining': validated_data.pop('date_of_joining', None),
            'address': validated_data.pop('address', None),
            'bank_name': validated_data.pop('bank_name', None),
            'bank_account_number': validated_data.pop('bank_account_number', None),
            'ifsc_code': validated_data.pop('ifsc_code', None)
        }

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        user = super().create(validated_data)
        user.groups.set(groups_data)
        self._update_user_permissions(user)

        # Create UserProfile with employee data
        UserProfile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            **{k: v for k, v in profile_data.items() if v is not None}
        )

        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', [])
        profile_data = {
            'contact_no': validated_data.pop('contact_no', None),
            'department_id': validated_data.pop('department', None),
            'designation': validated_data.pop('designation', None),
            'date_of_joining': validated_data.pop('date_of_joining', None),
            'address': validated_data.pop('address', None),
            'bank_name': validated_data.pop('bank_name', None),
            'bank_account_number': validated_data.pop('bank_account_number', None),
            'ifsc_code': validated_data.pop('ifsc_code', None)
        }

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        instance = super().update(instance, validated_data)
        instance.groups.set(groups_data)
        self._update_user_permissions(instance)

        # Update UserProfile
        profile, created = UserProfile.objects.get_or_create(user=instance)
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        
        for key, value in profile_data.items():
            if value is not None:
                setattr(profile, key, value)
        
        profile.save()

        return instance

    def _update_user_permissions(self, user):
        permissions = set()
        for group in user.groups.all():
            permissions.update(group.permissions.all())
        user.user_permissions.set(permissions)

    def get_department_name(self, obj):
        try:
            profile = obj.userprofile
            if profile.department_id:
                dept = Department.objects.get(id=profile.department_id)
                return dept.name
        except (UserProfile.DoesNotExist, Department.DoesNotExist):
            pass
        return None

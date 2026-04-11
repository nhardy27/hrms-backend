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
    # Extra write-only fields sourced from UserProfile, not part of User model
    contact_no = serializers.CharField(max_length=15, required=False)
    department = serializers.UUIDField(required=False)
    designation = serializers.UUIDField(required=False)
    designation_name = serializers.SerializerMethodField()  # Resolved via UserProfile.designation FK
    date_of_joining = serializers.DateField(required=False)
    address = serializers.CharField(required=False)
    bank_name = serializers.CharField(max_length=100, required=False)
    bank_account_number = serializers.CharField(max_length=30, required=False)
    ifsc_code = serializers.CharField(max_length=20, required=False)
    basic_salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    hra = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    allowance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    department_name = serializers.SerializerMethodField()  # Read-only department name resolved from FK
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups', 'is_staff', 'is_active', 'contact_no', 'department', 'department_name', 'designation', 'designation_name', 'date_of_joining', 'address', 'bank_name', 'bank_account_number', 'ifsc_code', 'basic_salary', 'hra', 'allowance']
        extra_kwargs = {
            'password': {'write_only': True}  # Never expose password in response
        }

    def to_representation(self, instance):
        # Append UserProfile fields to the default User representation
        representation = super().to_representation(instance)
        
        try:
            profile = instance.userprofile  # Access related UserProfile via reverse OneToOne
            representation['emp_code'] = profile.emp_code
            representation['contact_no'] = profile.contact_no
            representation['department'] = str(profile.department_id) if profile.department_id else None
            representation['department_name'] = self.get_department_name(instance)
            representation['designation'] = str(profile.designation_id) if profile.designation_id else None
            representation['designation_name'] = profile.designation.name if profile.designation else None
            representation['date_of_joining'] = profile.date_of_joining
            representation['address'] = profile.address
            representation['bank_name'] = profile.bank_name
            representation['bank_account_number'] = profile.bank_account_number
            representation['ifsc_code'] = profile.ifsc_code
            representation['basic_salary'] = profile.basic_salary
            representation['hra'] = profile.hra
            representation['allowance'] = profile.allowance
        except UserProfile.DoesNotExist:
            # Return None for all profile fields if UserProfile not yet created
            representation['emp_code'] = None
            representation['contact_no'] = None
            representation['department'] = None
            representation['department_name'] = None
            representation['designation'] = None
            representation['designation_name'] = None
            representation['date_of_joining'] = None
            representation['address'] = None
            representation['bank_name'] = None
            representation['bank_account_number'] = None
            representation['ifsc_code'] = None
            representation['basic_salary'] = None
            representation['hra'] = None
            representation['allowance'] = None

        return representation

    def create(self, validated_data):
        # Separate UserProfile fields before creating the User instance
        groups_data = validated_data.pop('groups', [])
        profile_data = {
            'contact_no': validated_data.pop('contact_no', None),
            'department_id': validated_data.pop('department', None),
            'designation_id': validated_data.pop('designation', None),
            'date_of_joining': validated_data.pop('date_of_joining', None),
            'address': validated_data.pop('address', None),
            'bank_name': validated_data.pop('bank_name', None),
            'bank_account_number': validated_data.pop('bank_account_number', None),
            'ifsc_code': validated_data.pop('ifsc_code', None),
            'basic_salary': validated_data.pop('basic_salary', None),
            'hra': validated_data.pop('hra', None),
            'allowance': validated_data.pop('allowance', None)
        }

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])  # Hash before saving
        
        user = super().create(validated_data)
        user.groups.set(groups_data)
        self._update_user_permissions(user)

        # Create linked UserProfile, skipping None values to preserve model defaults
        UserProfile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            **{k: v for k, v in profile_data.items() if v is not None}
        )

        return user

    def update(self, instance, validated_data):
        # Separate UserProfile fields before updating the User instance
        groups_data = validated_data.pop('groups', [])
        profile_data = {
            'contact_no': validated_data.pop('contact_no', None),
            'department_id': validated_data.pop('department', None),
            'designation_id': validated_data.pop('designation', None),
            'date_of_joining': validated_data.pop('date_of_joining', None),
            'address': validated_data.pop('address', None),
            'bank_name': validated_data.pop('bank_name', None),
            'bank_account_number': validated_data.pop('bank_account_number', None),
            'ifsc_code': validated_data.pop('ifsc_code', None),
            'basic_salary': validated_data.pop('basic_salary', None),
            'hra': validated_data.pop('hra', None),
            'allowance': validated_data.pop('allowance', None)
        }

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])  # Hash before saving

        instance = super().update(instance, validated_data)
        instance.groups.set(groups_data)
        self._update_user_permissions(instance)

        # get_or_create ensures UserProfile exists even if it was missing
        profile, created = UserProfile.objects.get_or_create(user=instance)
        profile.first_name = instance.first_name  # Keep UserProfile name in sync with User
        profile.last_name = instance.last_name
        
        for key, value in profile_data.items():
            if value is not None:  # Skip None to avoid overwriting existing values with empty input
                setattr(profile, key, value)
        
        profile.save()

        return instance

    def _update_user_permissions(self, user):
        # Aggregate all permissions from assigned groups and apply directly to user
        permissions = set()
        for group in user.groups.all():
            permissions.update(group.permissions.all())
        user.user_permissions.set(permissions)

    def get_designation_name(self, obj):
        # Return designation name string to avoid exposing raw UUID in response
        try:
            profile = obj.userprofile
            return profile.designation.name if profile.designation else None
        except UserProfile.DoesNotExist:
            return None

    def get_department_name(self, obj):
        # Lookup department name by UUID stored in UserProfile
        try:
            profile = obj.userprofile
            if profile.department_id:
                dept = Department.objects.get(id=profile.department_id)
                return dept.name
        except (UserProfile.DoesNotExist, Department.DoesNotExist):
            pass
        return None

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups', 'is_staff','is_active']
        #fields ='__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        # Hash the password before saving the user
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        user = super(UserSerializer, self).create(validated_data)
        user.groups.set(groups_data)
        self._update_user_permissions(user)
        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', [])
        # Hash the password before saving the user
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        instance = super(UserSerializer, self).update(instance, validated_data)
        instance.groups.set(groups_data)
        self._update_user_permissions(instance)
        return instance

    def _update_user_permissions(self, user):
        permissions = set()
        for group in user.groups.all():
            permissions.update(group.permissions.all())
        user.user_permissions.set(permissions)

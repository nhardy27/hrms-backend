from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from api.UserProfile.model import UserProfile


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all()
    )
    contact_No = serializers.IntegerField(required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups', 'is_staff','is_active', 'contact_No']
        #fields ='__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        # Get the original serialized data
        representation = super(UserSerializer, self).to_representation(instance)

        # Retrieve the UserProfile's contact_No and add it to the representation
        try:
            representation['contact_No'] = instance.userprofile.contact_No
        except UserProfile.DoesNotExist:
            representation['contact_No'] = None

        return representation

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        contact_No = validated_data.pop('contact_No', None)

        # Hash the password before saving the user
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        # Create the user
        user = super(UserSerializer, self).create(validated_data)
        
        # Set the groups for the user
        user.groups.set(groups_data)
        self._update_user_permissions(user)

        # Create the UserProfile linked to the user
        if contact_No is not None:
            UserProfile.objects.create(user=user, contact_No=contact_No)

        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', [])
        contact_No = validated_data.pop('contact_No', None)

        # Hash the password before saving the user
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        # Update the user instance
        instance = super(UserSerializer, self).update(instance, validated_data)
        
        # Update the groups for the user
        instance.groups.set(groups_data)
        self._update_user_permissions(instance)

        # Update or create UserProfile linked to the user
        if contact_No is not None:
            UserProfile.objects.update_or_create(user=instance, defaults={'contact_No': contact_No})

        return instance

    def _update_user_permissions(self, user):
        permissions = set()
        for group in user.groups.all():
            permissions.update(group.permissions.all())
        user.user_permissions.set(permissions)
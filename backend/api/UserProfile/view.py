from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.UserProfile.model import UserProfile
from backend.api.UserProfile.serializer import UserProfileSerializer
from api.permissions import CustomPermission

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [CustomPermission]

    def create(self, request, *args, **kwargs):
        data = request.data

        # 1️⃣ Create Django User
        user = User.objects.create_user(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password", "Emp@123"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name")
        )

        # 2️⃣ Create UserProfile (Employee)
        profile = UserProfile.objects.create(
            user=user,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            department_id=data.get("department"),
            contact_no=data.get("contact_no"),
            designation=data.get("designation"),
            date_of_joining=data.get("date_of_joining"),
            status=data.get("status", True)
        )

        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        user = profile.user
        data = request.data

        # 1️⃣ Update User table
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.save()

        # 2️⃣ Update UserProfile table
        serializer = self.get_serializer(
            profile,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

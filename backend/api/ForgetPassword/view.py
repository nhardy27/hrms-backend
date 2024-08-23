# api/ForgetPassword/view.py

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from django.conf import settings

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.BASE_URL}/api/v1/passwordResetConfirm/{uid}/{token}/"


            # Store the reset link in a variable
            click_this_link = reset_link

            # Send HTML email
            subject = "Password Reset Request"
            visible_token_part = f"/{token}/"
            message = (
                f"Hi {user.username},<br><br>"
                f"You requested a password reset. Click the link below to reset your password:<br>"
                f'<a href="{click_this_link}">{visible_token_part}</a><br><br>'
                "If you did not request this, please ignore this email.<br><br>"
                "Thank you."
            )
            email = EmailMessage(subject, message, to=[user.email])
            email.content_subtype = "html"  # Set the email content type to HTML
            email.send()

        return Response(
            {"detail": "If an account with this email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        # Extract new_password from the request body
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            # Decode the UID from base64 and check the token
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({"detail": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

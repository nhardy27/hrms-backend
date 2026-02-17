from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import traceback


from .model import Salary
from .serializer import SalarySerializer


class SalaryViewSet(viewsets.ModelViewSet):
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Salary.objects.filter(deleted_at__isnull=True)

        return Salary.objects.filter(
            attendance__user=user,
            deleted_at__isnull=True
        )

    @action(detail=True, methods=['post'])
    def send_email(self, request, pk=None):
        print(f"\n========== SEND EMAIL START ==========")
        print(f"[INFO] Request received for Salary ID: {pk}")

        try:
            salary = Salary.objects.select_related(
                'attendance__user', 'year'
            ).get(id=pk, deleted_at__isnull=True)

            print(f"[INFO] Salary record found: ID={salary.id}")

        except Salary.DoesNotExist:
            print(f"[ERROR] Salary record NOT found for ID: {pk}")
            print("========== SEND EMAIL END ==========\n")
            return Response(
                {"error": "Salary record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not salary.attendance:
            print(f"[WARNING] Attendance not linked for Salary ID: {pk}")
            print("========== SEND EMAIL END ==========\n")
            return Response(
                {"error": "Attendance not linked to salary"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = salary.attendance.user

        if not user:
            print(f"[WARNING] User not found in attendance for Salary ID: {pk}")
            print("========== SEND EMAIL END ==========\n")
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.email:
            print(f"[WARNING] Email not found for User ID: {user.id}")
            print("========== SEND EMAIL END ==========\n")
            return Response(
                {"error": "Employee email not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        subject = f"Salary Slip - {salary.month}/{salary.year.year}"
        print(f"[INFO] Preparing email for: {user.email}")
        print(f"[INFO] Subject: {subject}")

        try:
            html_content = render_to_string(
                'emails/salary_slip.html',
                {'salary': salary, 'user': user}
            )

            email = EmailMultiAlternatives(
                subject=subject,
                body=f"Salary Slip - {salary.month}/{salary.year.year}",
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            print(f"[SUCCESS] Email sent successfully to {user.email}")
            print("========== SEND EMAIL END ==========\n")

            return Response(
                {"message": "Email sent successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"[ERROR] Failed to send email for Salary ID: {salary.id}")
            print(f"[ERROR DETAILS] {str(e)}")
            print(traceback.format_exc())
            print("========== SEND EMAIL END ==========\n")

            return Response(
                {
                    "error": "Failed to send email",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

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
        try:
            salary = Salary.objects.select_related('attendance__user', 'year').get(id=pk, deleted_at__isnull=True)
        except Salary.DoesNotExist:
            return Response(
                {"error": "Salary record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not salary.attendance:
            return Response(
                {"error": "Attendance not linked to salary"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = salary.attendance.user
        if not user or not user.email:
            return Response(
                {"error": "Employee email not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        subject = f"Salary Slip - {salary.month}/{salary.year.year}"
        html_content = render_to_string('emails/salary_slip.html', {'salary': salary, 'user': user})

        try:
            email = EmailMultiAlternatives(
                subject,
                f"Salary Slip - {salary.month}/{salary.year.year}",
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            return Response(
                {"message": "Email sent successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            import traceback
            return Response(
                {"error": f"Failed to send email: {str(e)}", "details": traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

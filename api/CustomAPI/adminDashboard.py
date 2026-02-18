import json
from decimal import Decimal
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth.models import User
from django.http import HttpResponse
from api.Department.model import Department
from api.Attendance.model import Attendance
from api.AttendanceStatus.model import AttendanceStatus
from api.Leave.model import Leave
from api.salary.model import Salary


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            today = timezone.localdate()
            current_month = today.month
            current_year = today.year

            total_employee = User.objects.filter(
                is_active=True,
                is_superuser=False
            ).count()

            total_department = Department.objects.filter(
                status=True
            ).count()

            today_attendances = Attendance.objects.filter(
                date=today,
                check_in__isnull=False
            ).select_related('attendance_status')

            present_today = 0
            for attendance in today_attendances:
                if attendance.attendance_status:
                    if attendance.attendance_status.status in ['present', 'halfday']:
                        present_today += 1

            pending_leaves = Leave.objects.filter(
                status="PENDING",
                deleted_at__isnull=True
            ).count()

            # Get all active employees
            active_employees = User.objects.filter(
                is_active=True,
                is_superuser=False
            )

            paid_count = 0
            unpaid_count = 0

            for employee in active_employees:
                # Check if employee has paid salary for current month
                has_paid_salary = Salary.objects.filter(
                    attendance__user=employee,
                    month=current_month,
                    year__year=current_year,
                    payment_status="paid",
                    deleted_at__isnull=True
                ).exists()

                if has_paid_salary:
                    paid_count += 1
                else:
                    unpaid_count += 1

            total_paid_salaries = paid_count
            total_unpaid_salaries = unpaid_count

            employee_salaries = Salary.objects.filter(
                deleted_at__isnull=True
            ).select_related('attendance__user').values(
                'attendance__user__username',
                'attendance__user__first_name',
                'attendance__user__last_name',
                'month',
                'year__year',
                'net_salary',
                'payment_status'
            )[:10]

            data = {
                "total_employees": total_employee,
                "total_departments": total_department,
                "present_today": present_today,
                "pending_leaves": pending_leaves,
                "total_paid_salaries": total_paid_salaries,
                "total_unpaid_salaries": total_unpaid_salaries,
                "employee_salaries": list(employee_salaries)
            }

            return HttpResponse(
                json.dumps(data, indent=4, cls=DecimalEncoder),
                content_type="application/json",
                status=200
            )

        except Exception as e:
            return Response(
                {
                    "error": "Failed to load admin dashboard data",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from .model import Attendance
from .serializer import AttendanceSerializer
from api.AttendanceStatus.model import AttendanceStatus


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Attendance management.
    Provides CRUD operations with filtering, searching, and ordering.
    Supports filtering by date, user, status, emp_code, year, and month.
    """
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    # Configure filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'user', 'attendance_status']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering_fields = ['date', 'check_in', 'check_out']
    ordering = ['-date']  # Default ordering by date descending

    def get_queryset(self):
        """
        Get attendance records with custom filtering:
        - Superuser: can see all attendance records
        - Normal user: can only see their own attendance
        - Supports filtering by emp_code, year, and month
        """
        user = self.request.user

        # Optimize query with select_related to reduce database hits
        queryset = Attendance.objects.select_related(
            "user",
            "attendance_status",
            "user__userprofile"
        ).filter(deleted_at__isnull=True)  # Exclude soft-deleted records

        # Get query parameters for custom filtering
        emp_code = self.request.query_params.get("emp_code")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")

        # Filter by employee code
        if emp_code:
            queryset = queryset.filter(
                user__userprofile__emp_code__iexact=emp_code
            )

        # Filter by year
        if year:
            queryset = queryset.filter(date__year=year)

        # Filter by month name (e.g., "january")
        if month:
            import calendar
            try:
                month_number = list(calendar.month_name).index(month.capitalize())
                queryset = queryset.filter(date__month=month_number)
            except ValueError:
                pass

        # Restrict non-superuser to their own records
        if not user.is_superuser:
            queryset = queryset.filter(user=user)

        return queryset


    def perform_create(self, serializer):
        """
        Auto-assign 'absent' status if not provided during creation.
        """
        if not serializer.validated_data.get("attendance_status"):
            try:
                absent_status = AttendanceStatus.objects.get(status="absent")
                serializer.save(attendance_status=absent_status)
            except AttendanceStatus.DoesNotExist:
                serializer.save()
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete attendance record.
        Only superuser or the record owner can delete.
        """
        instance = self.get_object()

        # Check permission: only superuser or owner can delete
        if not request.user.is_superuser and instance.user != request.user:
            return Response(
                {"detail": "You are not allowed to delete this attendance"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Soft delete by setting deleted_at timestamp
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])

        return Response(
            {"message": "Attendance deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
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
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'user', 'attendance_status']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering_fields = ['date', 'check_in', 'check_out']
    ordering = ['-date']

    def get_queryset(self):
        user = self.request.user

        queryset = Attendance.objects.select_related(
            "user",
            "attendance_status"
        ).filter(deleted_at__isnull=True)

        if user.is_superuser:
            return queryset

        return queryset.filter(user=user)

    def perform_create(self, serializer):
        """
        Auto assign absent if not provided
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
        instance = self.get_object()

        if not request.user.is_superuser and instance.user != request.user:
            return Response(
                {"detail": "You are not allowed to delete this attendance"},
                status=status.HTTP_403_FORBIDDEN
            )

        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])

        return Response(
            {"message": "Attendance deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], url_path='search')
    def search_attendance(self, request):
        emp_code = request.query_params.get('emp_code')
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not emp_code or not year or not month:
            return Response(
                {"error": "emp_code, year, and month are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        month_map = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }

        month_num = month_map.get(month.lower())
        if not month_num:
            return Response(
                {"error": "Invalid month name"},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = Attendance.objects.select_related(
            "user", "attendance_status"
        ).filter(
            deleted_at__isnull=True,
            user__username=emp_code,
            date__year=year,
            date__month=month_num
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

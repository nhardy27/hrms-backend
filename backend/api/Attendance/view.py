
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.utils import timezone
# from rest_framework.permissions import IsAuthenticated

# from .model import Attendance
# from .serializer import AttendanceSerializer


# class AttendanceViewSet(viewsets.ModelViewSet):
#     serializer_class = AttendanceSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """
#         Return attendance of ONLY logged-in user
#         """
#         user = self.request.user

#         return Attendance.objects.filter(
#             user=user,
#             deleted_at__isnull=True
#         )

#     def destroy(self, request, *args, **kwargs):
#         """
#         Soft delete attendance (only own records)
#         """
#         instance = self.get_object()

#         # Extra safety: user can delete only his own data
#         if instance.user != request.user:
#             return Response(
#                 {"detail": "You are not allowed to delete this attendance"},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         instance.deleted_at = timezone.now()
#         instance.save(update_fields=["deleted_at"])

#         return Response(
#             {"message": "Attendance deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from .model import Attendance
from .serializer import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Superuser -> all attendance
        Normal user -> only own attendance
        """
        user = self.request.user

        if user.is_superuser:
            return Attendance.objects.filter(
                deleted_at__isnull=True
            )

        return Attendance.objects.filter(
            user=user,
            deleted_at__isnull=True
        )

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete attendance
        Superuser -> can delete any record
        Normal user -> can delete only own record
        """
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

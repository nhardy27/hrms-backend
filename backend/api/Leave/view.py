# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .model import Leave
# from .serializer import LeaveSerializer


# class LeaveViewSet(viewsets.ModelViewSet):
#     queryset = Leave.objects.filter(deleted_at__isnull=True)
#     serializer_class = LeaveSerializer

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.deleted_at = instance.updated_at
#         instance.save()
#         return Response(
#             {"message": "Leave deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .model import Leave
from .serializer import LeaveSerializer


class LeaveViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Superuser → sabhi leave
        if user.is_superuser:
            return Leave.objects.filter(deleted_at__isnull=True)

        # Normal user → sirf apni leave
        return Leave.objects.filter(
            user=user,
            deleted_at__isnull=True
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = instance.updated_at  # soft delete
        instance.save()
        return Response(
            {"message": "Leave deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

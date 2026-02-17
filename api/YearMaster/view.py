from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from .model import YearMaster
from .serializer import YearMasterSerializer


class YearMasterViewSet(viewsets.ModelViewSet):
    queryset = YearMaster.objects.filter(deleted_at__isnull=True)
    serializer_class = YearMasterSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(
            {"message": "Year deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

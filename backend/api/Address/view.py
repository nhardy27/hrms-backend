from rest_framework.viewsets import ModelViewSet
from api.Address.model import Address
from api.Address.serializer import AddressSerializer


class AddressViewset(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

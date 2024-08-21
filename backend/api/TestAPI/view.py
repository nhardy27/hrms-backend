from rest_framework.viewsets import ModelViewSet
from api.TestAPI.model import Test
from api.TestAPI.serializer import TestSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class TestViewset(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'description']
    search_fields = ['name', 'description']

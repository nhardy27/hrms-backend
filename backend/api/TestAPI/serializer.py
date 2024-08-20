from rest_framework import serializers
from api.TestAPI.model import Test
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        fields="__all__"
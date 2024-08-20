from rest_framework import serializers
from api.TestAPI.model import Test

class TestSerializer(serializers.ModelSerializer):
    address_title = serializers.SerializerMethodField()
    class Meta:
        model=Test
        # fields="__all__"
        fields = [
            'id',
            'name',
            'description',
            'address',
            'address_title',
        ]

    def get_address_title(self, obj):
        if obj.address:
            return obj.address.address
        return None
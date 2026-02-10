from rest_framework import serializers
from .model import YearMaster


class YearMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearMaster
        fields = "__all__"

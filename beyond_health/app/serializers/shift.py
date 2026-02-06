from rest_framework import serializers

from beyond_health.db.models import Shift


class ShiftListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

from rest_framework import serializers

from beyond_health.db.models import Treatment


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'


class TreatmentLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'name']


class TreatmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'

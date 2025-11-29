from rest_framework import serializers

from treatments.models import Treatment


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'


class TreatmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'

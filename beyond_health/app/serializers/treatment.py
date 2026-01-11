from rest_framework import serializers

from beyond_health.db.models import Treatment, TreatmentPlanItem


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
        fields = [
            'id',
            'name',
            'category',
            'description',
            'duration',
            'cost',
            'is_active',
        ]


class TreatmentPlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlanItem
        fields = '__all__'


class TreatmentPlanItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlanItem
        fields = [
            'id',
            'quantity',
            'cost',
            'notes',
            'tooth_number',
        ]

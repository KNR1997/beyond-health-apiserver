from rest_framework import serializers

from beyond_health.db.models import Treatment, TreatmentPlanItem, TreatmentPlan


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


class TreatmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlan
        fields = '__all__'


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


class TreatmentPlanListSerializer(serializers.ModelSerializer):
    items = TreatmentPlanItemListSerializer(many=True)

    class Meta:
        model = TreatmentPlan
        fields = [
            'id',
            'name',
            'description',
            'status',
            'total_cost',
            'items',
        ]

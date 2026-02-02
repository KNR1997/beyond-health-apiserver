from rest_framework import serializers

from beyond_health.app.serializers.dentist import DentistListSerializer
from beyond_health.app.serializers.patient import PatientListSerializer
from beyond_health.db.models import Treatment, TreatmentPlan, TreatmentPlanItem


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


class TreatmentPlanListSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()
    dentist = DentistListSerializer()

    class Meta:
        model = TreatmentPlan
        fields = [
            'id',
            'name',
            'description',
            'status',
            'total_cost',
            'description',
            'patient',
            'dentist',
        ]


class TreatmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlan
        fields = '__all__'


class TreatmentPlanItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlanItem
        fields = '__all__'


class TreatmentPlanItemCustomSerializer(serializers.Serializer):
    treatment_id = serializers.UUIDField()
    tooth_number = serializers.CharField()
    cost = serializers.FloatField()
    note = serializers.CharField()


class TreatmentPlanItemsCreateSerializer(serializers.Serializer):
    treatment_plan_id = serializers.UUIDField()
    items = TreatmentPlanItemCustomSerializer(many=True)

    def create(self, validated_data):
        for item in validated_data['items']:
            TreatmentPlanItem.objects.create(
                treatment_plan_id = validated_data['treatment_plan_id'],
                treatment_id = item['treatment_id'],
                tooth_number = item['tooth_number'],
                cost=item['cost'],
                notes=item['note'],
            )

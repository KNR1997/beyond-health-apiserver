from decimal import Decimal

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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
        fields = [
            'id',
            'name',
            'category',
            'description',
            'duration',
            'cost',
            'is_active',
        ]


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
    treatment = TreatmentListSerializer()

    class Meta:
        model = TreatmentPlanItem
        fields = [
            'id',
            'quantity',
            'cost',
            'notes',
            'tooth_number',
            'treatment',
        ]


class TreatmentPlanItemCustomSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False, allow_null=True)
    treatment_id = serializers.UUIDField()
    tooth_number = serializers.CharField()
    cost = serializers.FloatField()
    notes = serializers.CharField()


class TreatmentPlanItemsCreateSerializer(serializers.Serializer):
    treatment_plan_id = serializers.UUIDField()
    items = TreatmentPlanItemCustomSerializer(many=True)

    def create(self, validated_data):
        for item in validated_data['items']:
            TreatmentPlanItem.objects.create(
                treatment_plan_id=validated_data['treatment_plan_id'],
                treatment_id=item['treatment_id'],
                tooth_number=item['tooth_number'],
                cost=item['cost'],
                notes=item['notes'],
            )

    def update(self, instance, validated_data):

        # Get TreatmentPlan related to items
        treatment_plan = get_object_or_404(
            TreatmentPlan,
            pk=validated_data['treatment_plan_id']
        )

        # Reset total_cost before recalculating
        treatment_plan.total_cost = Decimal('0.00')

        for item in validated_data['items']:
            cost = Decimal(str(item['cost']))

            if item['id']:
                treatment_plan_item = get_object_or_404(TreatmentPlanItem, pk=item['id'])
                if treatment_plan_item:
                    treatment_plan_item.treatment_id = item['treatment_id']
                    treatment_plan_item.tooth_number = item['tooth_number']
                    treatment_plan_item.cost = item['cost']
                    treatment_plan_item.notes = item['notes']

                    treatment_plan_item.save()
            else:
                TreatmentPlanItem.objects.create(
                    treatment_plan_id=validated_data['treatment_plan_id'],
                    treatment_id=item['treatment_id'],
                    tooth_number=item['tooth_number'],
                    cost=item['cost'],
                    notes=item['notes'],
                )
            # Sum total_cost
            treatment_plan.total_cost += cost

        treatment_plan.save()
        return treatment_plan

from rest_framework import serializers

from beyond_health.app.serializers.dentist import DentistListSerializer
from beyond_health.app.serializers.patient import PatientListSerializer
from beyond_health.db.models import Treatment, TreatmentPlan


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

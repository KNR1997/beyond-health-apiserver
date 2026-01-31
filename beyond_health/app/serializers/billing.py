from beyond_health.app.serializers.base import BaseSerializer
from beyond_health.app.serializers.patient import PatientListSerializer
from beyond_health.app.serializers.treatment import TreatmentPlanListSerializer
from beyond_health.db.models.billing import Billing


class BillingListSerializer(BaseSerializer):
    patient = PatientListSerializer()
    treatment_plan = TreatmentPlanListSerializer()

    class Meta:
        model = Billing
        fields = [
            'id',
            'invoice_number',
            'total_amount',
            'insurance_covered',
            'patient_balance',
            'status',
            'due_date',
            'paid_at',
            'patient',
            'treatment_plan',
        ]

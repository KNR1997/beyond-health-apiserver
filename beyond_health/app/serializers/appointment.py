from beyond_health.app.serializers.base import BaseSerializer
from beyond_health.db.models.appointment import Appointment
from beyond_health.app.serializers.patient import PatientListSerializer
from beyond_health.app.serializers.dentist import DentistListSerializer


class AppointmentListSerializer(BaseSerializer):
    patient = PatientListSerializer()
    dentist = DentistListSerializer()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'appointment_no',
            'appointment_date',
            'duration',
            'reason_for_visit',
            'appointment_type',
            'status',

            'patient',
            'dentist',
        ]


class AppointmentCreateSerializer(BaseSerializer):
    class Meta:
        model = Appointment
        fields = [
            'patient',
            'dentist',
            'appointment_date',
            'appointment_type',
        ]


class AppointmentUpdateSerializer(BaseSerializer):
    class Meta:
        model = Appointment
        fields = [
            'patient',
            'dentist',
            'appointment_date',
            'appointment_type',
            'status',
        ]

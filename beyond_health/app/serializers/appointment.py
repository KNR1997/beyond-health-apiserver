from beyond_health.app.serializers.base import BaseSerializer
from beyond_health.db.models.appointment import Appointment


class AppointmentListSerializer(BaseSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'appointment_date',
            'duration',
            'reason_for_visit',
            'status'
        ]


class AppointmentCreateSerializer(BaseSerializer):
    class Meta:
        model = Appointment
        fields = [
            'patient',
            'appointment_date',
            'appointment_type',
        ]


class AppointmentUpdateSerializer(BaseSerializer):
    class Meta:
        model = Appointment
        fields = [
            'patient',
            'appointment_date',
            'appointment_type',
            'reason_for_visit',
            'status',
            'notes',
        ]

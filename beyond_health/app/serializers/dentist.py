from django.db import transaction
from rest_framework import serializers

from beyond_health.app.permissions.base import ROLE
from beyond_health.app.serializers.base import BaseSerializer
from beyond_health.db.models import Dentist, Patient, User


class DentistListSerializer(BaseSerializer):
    class Meta:
        model = Dentist
        fields = '__all__'


class DentistSerializer(BaseSerializer):
    class Meta:
        model = Dentist
        fields = '__all__'


class PatientListSerializer(BaseSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'mobile_number',
            'gender',
        ]


class PatientSerializer(BaseSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

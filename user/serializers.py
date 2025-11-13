from rest_framework import serializers

from authentication.models import User
from user.models import Patient, Dentist, Staff


class AdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile_number', 'email', 'display_name', 'first_name', 'last_name', 'is_active']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile_number', 'email', 'display_name', 'first_name', 'last_name', 'is_active']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class DentistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentist
        fields = '__all__'


class DentistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentist
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

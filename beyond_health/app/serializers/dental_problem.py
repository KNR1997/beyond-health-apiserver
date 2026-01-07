from rest_framework import serializers

from beyond_health.db.models import DentalProblem


class DentalProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalProblem
        fields = '__all__'


class DentalProblemLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalProblem
        fields = ['id', 'name']


class DentalProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalProblem
        fields = '__all__'

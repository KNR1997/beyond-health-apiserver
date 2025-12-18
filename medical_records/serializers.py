from rest_framework import serializers

from medical_records.models import Problem


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

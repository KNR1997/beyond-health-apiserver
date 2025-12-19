from rest_framework import serializers

from medical_records.models import Problem, PatientProblem
from user.models import Patient


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class PatientProblemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProblem
        fields = '__all__'


class PatientProblemItemSerializer(serializers.Serializer):
    problem = serializers.PrimaryKeyRelatedField(
        queryset=Problem.objects.filter(is_active=True)
    )
    severity = serializers.ChoiceField(
        choices=PatientProblem.Severity.choices,
        default=PatientProblem.Severity.MODERATE
    )
    notes = serializers.CharField(required=False, allow_blank=True)


class PatientProblemBulkCreateSerializer(serializers.Serializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all()
    )
    problems = PatientProblemItemSerializer(many=True)

    def validate(self, attrs):
        patient = attrs['patient']
        problems = attrs['problems']

        problem_ids = [item['problem'].id for item in problems]

        # Check duplicates in request
        if len(problem_ids) != len(set(problem_ids)):
            raise serializers.ValidationError(
                "Duplicate problems in request."
            )

        # Check existing problems for patient
        existing = PatientProblem.objects.filter(
            patient=patient,
            problem_id__in=problem_ids
        ).values_list('problem_id', flat=True)

        if existing:
            raise serializers.ValidationError(
                f"Problems already added: {list(existing)}"
            )

        return attrs

    def create(self, validated_data):
        patient = validated_data['patient']
        problems_data = validated_data['problems']

        patient_problems = [
            PatientProblem(
                patient=patient,
                problem=item['problem'],
                severity=item.get('severity', PatientProblem.Severity.MODERATE),
                notes=item.get('notes')
            )
            for item in problems_data
        ]

        # Efficient bulk insert
        return PatientProblem.objects.bulk_create(patient_problems)


class PatientProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProblem
        fields = '__all__'

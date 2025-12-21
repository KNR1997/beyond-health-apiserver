from django.db import transaction
from rest_framework import serializers

from medical_records.models import Problem, PatientProblem
from user.models import Patient


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class ProblemLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'name']


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class PatientProblemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProblem
        fields = '__all__'


class PatientProblemItemSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False, allow_null=True)
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
    deleted_problem_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        allow_empty=True,
    )

    def validate(self, attrs):
        patient = attrs['patient']
        problems = attrs['problems']
        deleted_ids = attrs.get('deleted_problem_ids', [])

        # Validate IDs belong to this patient
        ids = [item['id'] for item in problems if 'id' in item]

        existing = PatientProblem.objects.filter(
            id__in=ids,
            patient=patient
        ).values_list('id', flat=True)

        # if len(existing) != len(ids):
        #     raise serializers.ValidationError(
        #         "One or more PatientProblem IDs are invalid for this patient."
        #     )

        # Prevent duplicate problems in request
        problem_ids = [item['problem'].id for item in problems]
        if len(problem_ids) != len(set(problem_ids)):
            raise serializers.ValidationError(
                "Duplicate problems in request."
            )

        # ---- VALIDATE DELETED IDS ----
        if deleted_ids:
            delete_existing = set(
                PatientProblem.objects.filter(
                    id__in=deleted_ids,
                    patient=patient
                ).values_list('id', flat=True)
            )

            if len(delete_existing) != len(deleted_ids):
                raise serializers.ValidationError(
                    "One or more deleted_problem_ids are invalid for this patient."
                )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        patient = validated_data['patient']
        problems_data = validated_data['problems']
        deleted_ids = validated_data.get('deleted_problem_ids', [])

        # ---- DELETE ----
        if deleted_ids:
            PatientProblem.objects.filter(
                patient=patient,
                id__in=deleted_ids
            ).delete()

        to_create = []
        to_update = []

        existing_map = {
            pp.id: pp
            for pp in PatientProblem.objects.filter(
                patient=patient,
                id__in=[
                    item['id'] for item in problems_data if 'id' in item
                ]
            )
        }

        for item in problems_data:
            if item['id'] is not None:
                # UPDATE
                patient_problem = existing_map[item['id']]
                patient_problem.problem = item['problem']
                patient_problem.severity = item.get(
                    'severity', patient_problem.severity
                )
                patient_problem.notes = item.get(
                    'notes', patient_problem.notes
                )
                to_update.append(patient_problem)
            else:
                # CREATE
                to_create.append(
                    PatientProblem(
                        patient=patient,
                        problem=item['problem'],
                        severity=item.get(
                            'severity',
                            PatientProblem.Severity.MODERATE
                        ),
                        notes=item.get('notes')
                    )
                )

        if to_create:
            PatientProblem.objects.bulk_create(to_create)

        if to_update:
            PatientProblem.objects.bulk_update(
                to_update,
                ['problem', 'severity', 'notes']
            )

        return to_create + to_update


class PatientProblemBulkUpdateSerializer(serializers.Serializer):
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

    def update(self, instance, validated_data):
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
    problem = ProblemLiteSerializer()

    class Meta:
        model = PatientProblem
        fields = ['id', 'problem', 'severity']

from django.db import transaction
from rest_framework import serializers

from beyond_health.app.serializers.dental_problem import DentalProblemLiteSerializer
from beyond_health.db.models import PatientDentalProblem, Patient, DentalProblem


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PatientDentalProblemListSerializer(serializers.ModelSerializer):
    dental_problem = DentalProblemLiteSerializer()

    class Meta:
        model = PatientDentalProblem
        fields = ['id', 'dental_problem', 'severity']


class PatientDentalProblemItemSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False, allow_null=True)
    problem = serializers.PrimaryKeyRelatedField(
        queryset=DentalProblem.objects.filter(is_active=True)
    )
    severity = serializers.ChoiceField(
        choices=PatientDentalProblem.Severity.choices,
        default=PatientDentalProblem.Severity.MODERATE
    )
    notes = serializers.CharField(required=False, allow_blank=True)


class PatientProblemBulkCreateSerializer(serializers.Serializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all()
    )
    problems = PatientDentalProblemItemSerializer(many=True)
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

        existing = PatientDentalProblem.objects.filter(
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
                PatientDentalProblem.objects.filter(
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
            PatientDentalProblem.objects.filter(
                patient=patient,
                id__in=deleted_ids
            ).delete()

        to_create = []
        to_update = []

        existing_map = {
            pp.id: pp
            for pp in PatientDentalProblem.objects.filter(
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
                    PatientDentalProblem(
                        patient=patient,
                        problem=item['problem'],
                        severity=item.get(
                            'severity',
                            PatientDentalProblem.Severity.MODERATE
                        ),
                        notes=item.get('notes')
                    )
                )

        if to_create:
            PatientDentalProblem.objects.bulk_create(to_create)

        if to_update:
            PatientDentalProblem.objects.bulk_update(
                to_update,
                ['problem', 'severity', 'notes']
            )

        return to_create + to_update

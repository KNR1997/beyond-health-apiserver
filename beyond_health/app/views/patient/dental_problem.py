from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet, BaseAPIView
from beyond_health.app.serializers.dental_problem import DentalProblemListSerializer
from beyond_health.app.serializers.patient import PatientDentalProblemListSerializer, PatientProblemBulkCreateSerializer
from beyond_health.db.models import PatientDentalProblem, Patient, DentalProblem


# Create your views here.
class PatientDentalProblemViewSet(BaseViewSet):
    model = PatientDentalProblem
    serializer_class = PatientDentalProblemListSerializer

    search_fields = ["name"]
    filterset_fields = []

    def create(self, request, *args, **kwargs):
        serializer = PatientProblemBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient_problems = serializer.save()

        output = PatientDentalProblemListSerializer(
            patient_problems,
            many=True
        ).data

        return Response(output, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        patient_id = kwargs.get("pk")

        patient = get_object_or_404(Patient, pk=patient_id)

        patient_problems = (
            PatientDentalProblem.objects
            .filter(patient=patient)
            .select_related("problem")
        )

        serializer = self.get_serializer(
            patient_problems,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientDentalProblemStatusChangeEndpoint(BaseAPIView):
    def post(self, request):
        dental_problem_id = request.data["id"]
        dental_problem = get_object_or_404(DentalProblem, pk=dental_problem_id)

        if dental_problem.is_active:
            dental_problem.is_active = False
        else:
            dental_problem.is_active = True

        dental_problem.save()
        serializer = DentalProblemListSerializer(dental_problem)
        return Response(serializer.data, status=status.HTTP_200_OK)

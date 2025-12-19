from rest_framework import status
from rest_framework.response import Response

from core.views.base import BaseViewSet
from medical_records.serializers import PatientProblemListSerializer, PatientProblemBulkCreateSerializer


# Create your views here.
class PatientDentalProblemViewSet(BaseViewSet):
    serializer_class = PatientProblemBulkCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient_problems = serializer.save()

        output = PatientProblemListSerializer(
            patient_problems,
            many=True
        ).data

        return Response(output, status=status.HTTP_201_CREATED)

# Third party imports

from rest_framework import status
from rest_framework.response import Response

# Module imports
from beyond_health.app.views.base import BaseAPIView
from beyond_health.db.models import Patient, DentalProblem, Dentist


# Create your views here.
class AnalyticsDataEndpoint(BaseAPIView):
    def get(self, request):

        dentist_count = Dentist.objects.all().count()
        patient_count = Patient.objects.all().count()
        dental_problem_count = DentalProblem.objects.all().count()
        # active_enrollment_count = Enrollment.objects.filter(is_active=True).count()

        output = {
            "total_revenue": 0,
            "dentist_count": dentist_count,
            "patient_count": patient_count,
            "dental_problem_count": dental_problem_count,
            # "active_enrollment_count": enrollment_count,
        }


        return Response(output, status=status.HTTP_200_OK)
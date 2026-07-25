# Python imports
from calendar import month_name

# Django imports
from django.utils import timezone
from django.db.models.functions import TruncMonth

# Third party imports
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response

# Module imports
from beyond_health.app.views.base import BaseAPIView
from beyond_health.db.models import Patient, DentalProblem, Dentist, Appointment


# Create your views here.
class AnalyticsDataEndpoint(BaseAPIView):
    def get(self, request):

        dentist_count = Dentist.objects.all().count()
        patient_count = Patient.objects.all().count()
        dental_problem_count = DentalProblem.objects.all().count()

        # Get enrollments by month for the current year
        current_year = timezone.now().year
        appointments_by_month = (
            Appointment.objects
            .filter(created_at__year=current_year)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )

        # Create a dict for easy lookup
        appointments_dict = {entry['month'].month: entry['total']
                             for entry in appointments_by_month}

        # Fill in all months (including those with 0 appointments)
        formatted_appointments_by_month = []
        for month_num in range(1, 13):
            formatted_appointments_by_month.append({
                'month': month_name[month_num],
                'total': appointments_dict.get(month_num, 0)
            })

        output = {
            "total_revenue": 0,
            "dentist_count": dentist_count,
            "patient_count": patient_count,
            "dental_problem_count": dental_problem_count,
            "appointments_by_month": formatted_appointments_by_month,
            # "schedule_appointment_count": schedule_appointment_count,
        }

        return Response(output, status=status.HTTP_200_OK)

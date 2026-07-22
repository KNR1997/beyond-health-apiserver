from django.urls import path

from beyond_health.app.views.report.dentist import DentistPdfView
from beyond_health.app.views.report.patient_registration import PatientRegistrationPdfView
from beyond_health.db.models import Dentist

urlpatterns = [
    path(
        "reports/patient-registration/",
        PatientRegistrationPdfView.as_view(),
        name="patient-registration",
    ),

    path(
        "reports/dentist/",
        DentistPdfView.as_view(),
        name="dentist",
    ),


]
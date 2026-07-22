from django.urls import path

from beyond_health.app.views.report.dental_problem import DentalProblemPdfView
from beyond_health.app.views.report.dentist import DentistPdfView
from beyond_health.app.views.report.patient_registration import PatientRegistrationPdfView
from beyond_health.app.views.report.treatments import TreatmentPdfView

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

    path(
        "reports/treatment/",
        TreatmentPdfView.as_view(),
        name="treatment",
    ),

    path(
        "reports/dental-problem/",
        DentalProblemPdfView.as_view(),
        name="dental-problem",
    ),


]
from django.urls import path

from beyond_health.app.views.report.appointment import AppointmentPdfView
from beyond_health.app.views.report.dental_problem import DentalProblemPdfView
from beyond_health.app.views.report.dentist import DentistPdfView
from beyond_health.app.views.report.patient_registration import PatientRegistrationPdfView
from beyond_health.app.views.report.treatment_plans import TreatmentPlanPdfView
from beyond_health.app.views.report.treatments import TreatmentPdfView
from beyond_health.app.views.report.roster import RosterPdfView

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

    path(
        "reports/appointment/",
        AppointmentPdfView.as_view(),
        name="appointment",
    ),

    path(
        "reports/treatment-plan/",
        TreatmentPlanPdfView.as_view(),
        name="treatment-plan",
    ),

    path(
        "reports/roster/<uuid:pk>",
        RosterPdfView.as_view(),
        name="roster-report",
    ),
]

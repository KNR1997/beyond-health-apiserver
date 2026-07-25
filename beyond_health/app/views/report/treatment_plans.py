from io import BytesIO

from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

from beyond_health.db.models import TreatmentPlan


class TreatmentPlanPdfView(APIView):

    def get(self, request):
        try:
            # Use select_related for ForeignKey/OneToOne relationships
            treatment_plans = TreatmentPlan.objects.all()
            # pdf = InvoicePdfService.generate(invoice)

            html = render_to_string(
                "treatment-plan.html",
                {
                    "treatment_plans": treatment_plans
                }
            )

            pdf_file = BytesIO()

            HTML(
                string=html
            ).write_pdf(
                target=pdf_file
            )

            pdf_file.seek(0)

            response = HttpResponse(
                pdf_file,
                content_type="application/pdf"
            )

            response[
                "Content-Disposition"
            ] = f'attachment; filename="treatment_plan.pdf"'

            return response


        except Exception as e:
            print(f"Error generating PDF: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
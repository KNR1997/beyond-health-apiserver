from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML
from beyond_health.db.models import RosterWeek, RosterAssignment, Shift, User
from beyond_health.app.permissions.base import ROLE


class RosterPdfView(APIView):

    def get(self, request, pk=None):
        try:
            # Get roster week ID from request
            roster_week_id = pk

            if not roster_week_id:
                return Response(
                    {"error": "roster_week_id parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch the roster week
            roster_week = RosterWeek.objects.get(id=roster_week_id)

            # Fetch all assignments for this roster week with related data
            roster_assignments = RosterAssignment.objects.filter(
                roster_week=roster_week
            ).select_related(
                'shift',
                'user'  # Changed from dentist/staff to user
            ).order_by(
                'date',
                # 'shift__code'
            )

            # Group assignments by date for better visualization
            assignments_by_date = {}
            for assignment in roster_assignments:
                date_str = assignment.date.strftime('%Y-%m-%d')
                if date_str not in assignments_by_date:
                    assignments_by_date[date_str] = []
                assignments_by_date[date_str].append(assignment)

            # Get all distinct users (both dentists and staff) from assignments
            users = User.objects.filter(
                id__in=roster_assignments.values_list('user_id', flat=True)
            ).distinct()

            # Separate users by role
            dentists = users.filter(role=ROLE.DENTIST.value)
            staff_members = users.filter(role=ROLE.STAFF.value)

            # Get all shifts for the week
            shifts = Shift.objects.filter(
                id__in=roster_assignments.values_list('shift_id', flat=True)
            ).distinct().order_by('code')

            # Calculate summary statistics
            total_assignments = roster_assignments.count()
            unique_days = len(assignments_by_date)

            # Get role names mapping
            role_names = {
                ROLE.DENTIST.value: 'Dentist',
                ROLE.STAFF.value: 'Staff',
                ROLE.ADMIN.value: 'Admin',
                ROLE.PATIENT.value: 'Patient',
                ROLE.GUEST.value: 'Guest'
            }

            # Generate PDF
            html = render_to_string(
                "roster-report.html",
                {
                    "roster_week": roster_week,
                    "roster_assignments": roster_assignments,
                    "assignments_by_date": assignments_by_date,
                    "dentists": dentists,
                    "staff_members": staff_members,
                    "users": users,
                    "shifts": shifts,
                    "total_assignments": total_assignments,
                    "unique_days": unique_days,
                    "generated_date": datetime.now(),
                    "clinic_name": "Beyond Health Dental Clinic",
                    "clinic_address": "Colombo, Sri Lanka",
                    "clinic_phone": "+94 11 277 5551",
                    # "role_names": role_names,
                }
            )

            pdf_file = BytesIO()

            HTML(
                string=html,
                base_url=request.build_absolute_uri('/')
            ).write_pdf(
                target=pdf_file,
                presentational_hints=True,
                stylesheets=None
            )

            pdf_file.seek(0)

            filename = f"roster_report_{roster_week}.pdf"

            response = HttpResponse(
                pdf_file,
                content_type="application/pdf"
            )

            response[
                "Content-Disposition"
            ] = f'attachment; filename="{filename}"'

            return response

        except RosterWeek.DoesNotExist:
            return Response(
                {"error": "Roster week not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet
from beyond_health.app.serializers import dentist
from beyond_health.app.serializers.appointment import AppointmentListSerializer, AppointmentCreateSerializer, \
    AppointmentUpdateSerializer
from beyond_health.db.models import Notification, UserNotification
from beyond_health.db.models.appointment import Appointment


class AppointmentViewSet(BaseViewSet):
    model = Appointment
    serializer_class = AppointmentListSerializer

    search_fields = ['patient__name']
    filterset_fields = ['patient', 'dentist', 'status']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return (
            self.filter_queryset(
                super().get_queryset().select_related('patient', 'dentist'))
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # @allow_permission([])
    def create(self, request, *args, **kwargs):
        serializer = AppointmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment = serializer.save()

        notification = Notification.objects.create(
            title="New Appointment Scheduled",
            message=f"Your Appointment with {appointment.dentist.user.first_name}. has been scheduled for {appointment.appointment_date:%d %b %Y} at {appointment.duration}..",
            type="GENERAL",
            priority="medium",
        )
        # Create user notification for the patient user
        UserNotification.objects.create(
            notification=notification,
            user=appointment.dentist.user
        )

        output = AppointmentListSerializer(
            appointment, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    # @allow_permission([])
    def update(self, request, *args, **kwargs):
        appointment = Appointment.objects.get(pk=kwargs["pk"])
        serializer = AppointmentUpdateSerializer(
            appointment,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()

        output = AppointmentListSerializer(
            appointment, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        appointment = Appointment.objects.get(pk=kwargs["pk"])
        appointment.delete(soft=False)
        return Response(status=status.HTTP_204_NO_CONTENT)

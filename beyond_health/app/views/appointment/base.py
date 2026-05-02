from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet
from beyond_health.app.serializers.appointment import AppointmentListSerializer, AppointmentCreateSerializer, \
    AppointmentUpdateSerializer
from beyond_health.db.models.appointment import Appointment


class AppointmentViewSet(BaseViewSet):
    model = Appointment
    serializer_class = AppointmentListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
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

        output = AppointmentListSerializer(appointment, context={"request": request}).data
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

        output = AppointmentListSerializer(appointment, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

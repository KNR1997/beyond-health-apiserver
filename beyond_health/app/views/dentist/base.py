# Third party imports
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet
from beyond_health.app.permissions.base import allow_permission, ROLE
from beyond_health.app.serializers.dentist import DentistListSerializer, DentistCreateSerializer, \
    DentistUpdateSerializer
from beyond_health.app.views.base import BaseAPIView
from beyond_health.db.models import Dentist
from beyond_health.db.models.notification import Notification, UserNotification


# Create your views here.
class DentistViewSet(BaseViewSet):
    model = Dentist
    serializer_class = DentistListSerializer

    search_fields = ['user__first_name', 'user__last_name']
    ordering_fields = ['user__first_name','specialization','license_number']
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        serializer = DentistCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dentist = serializer.save()

        notification = Notification.objects.create(
            title="Welcome Dentist",
            message=f"You have been added as a {dentist.user.first_name}. Please check your schedule.",
            type="GENERAL",
            priority="low",
        )
        # Create user notification for the dentist user
        UserNotification.objects.create(
            notification=notification,
            user=dentist.user
        )

        output = DentistListSerializer(dentist, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        dentist = Dentist.objects.get(pk=kwargs["pk"])
        serializer = DentistUpdateSerializer(
            dentist,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        dentist = serializer.save()

        output = DentistListSerializer(dentist, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DentistRestPasswordEndpoint(BaseAPIView):
    @allow_permission([ROLE.ADMIN])
    def post(self, request):
        dentist_id = request.data["dentist_id"]
        dentist = get_object_or_404(Dentist, pk=dentist_id)

        user = dentist.user

        user.set_password('1234')
        user.save()

        return Response(status=status.HTTP_200_OK)

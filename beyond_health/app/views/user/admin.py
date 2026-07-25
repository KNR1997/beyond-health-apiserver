# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from beyond_health.app.permissions.base import ROLE, allow_permission
from beyond_health.app.serializers.user import UserListSerializer
from beyond_health.app.views.base import BaseViewSet, BaseAPIView
from beyond_health.db.models import User
from beyond_health.app.serializers.authentication import ResetUserPasswordSerializer

logger = structlog.getLogger(__name__)


class AdminViewSet(BaseViewSet):
    model = User
    serializer_class = UserListSerializer

    search_fields = ["username", "email"]

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset().filter(role=ROLE.ADMIN.value))
        )
        logger.info("user_admin_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("admin_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)


class ResetUserPasswordEndpoint(BaseAPIView):
    @allow_permission([ROLE.ADMIN])
    def post(self, request, *args, **kwargs):
        logger.info("admin_rest_user_password_started", requested_by=request.user.id)

        serializer = ResetUserPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user_id = self.kwargs.get("user_id")

        user = User.objects.get(pk=user_id)

        user.set_password(serializer.validated_data.get("password"))

        user.save()

        logger.info("admin_rest_user_password_completed", user_id=user_id, created_by=request.user.id)
        return Response(status=status.HTTP_200_OK)

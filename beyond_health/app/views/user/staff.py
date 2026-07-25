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


class StaffViewSet(BaseViewSet):
    model = User
    serializer_class = UserListSerializer

    search_fields = ["username", "email"]

    def get_queryset(self):
        queryset = (
            self.filter_queryset(
                super().get_queryset().filter(role=ROLE.STAFF.value))
        )
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("staff_list_requested",
                    requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

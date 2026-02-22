from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet
from beyond_health.app.permissions.base import allow_permission, ROLE
from beyond_health.app.serializers.user import UserListSerializer, UserSerializer
from beyond_health.db.models import User


# Create your views here.
class UserViewSet(BaseViewSet):
    model = User
    serializer_class = UserListSerializer

    search_fields = ['first_name', 'last_name']
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN, ROLE.DENTIST])
    def update(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs["pk"])

        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        output = UserListSerializer(user, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

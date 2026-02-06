from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from beyond_health.app.permissions.base import ROLE
from beyond_health.app.permissions.permissions import IsAdminOrReadOnly
from .serializers import SignupSerializer, SigninSerializer, ChangePasswordSerializer
from beyond_health.app.views.base import BaseAPIView
from ..app.serializers.user import UserLiteSerializer


# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {'user': serializer.data, 'tokens': tokens},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                'tokens': get_tokens_for_user(user),
                'permissions': user.permissions,
                'role': user.role_name,
            },
            status=status.HTTP_200_OK
        )


class CreateAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.role = ROLE.ADMIN.value
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return Response(
            {"detail": "Admin user created successfully"},
            status=status.HTTP_201_CREATED
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserLiteSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(status=HTTP_200_OK)


class ChangePasswordEndpoint(BaseAPIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_200_OK)

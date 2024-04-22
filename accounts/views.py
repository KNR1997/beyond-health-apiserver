import datetime
import random

from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from accounts.utils import send_otp
from .models import UserAccount
from .serializers import ClientUserSerializer
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    UserModel View.
    """

    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()
        # password = request.data.get("password")  # Extract password from request data
        if (
                not instance.is_active
                # create profiles for user
                and instance.otp == request.data.get("otp")
                and instance.otp_expiry
                and timezone.now() < instance.otp_expiry
        ):
            # create access refresh token
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()

            # # Generate new tokens
            refresh = RefreshToken.for_user(instance)
            access_token = str(refresh.access_token)

            # Use CustomTokenObtainPairView to generate tokens
            # token_serializer = CustomTokenObtainPairSerializer(data={'username': instance.username,
            #                               'password': instance.password})
            # token_serializer = CustomTokenObtainPairSerializer(
            #     data={'phone_number': instance.phone_number,
            #           'email': instance.email, 
            #           'password': password
            #           })

            # token_serializer.is_valid(raise_exception=True)
            # tokens = token_serializer.validated_data

            # id = tokens['id']
            # email = tokens['email']
            # access_token = tokens['access']
            # refresh_token = tokens['refresh']

            return Response(
                {
                    "message": "Successfully verified the user.",
                    # "id": id,
                    # "email": email,
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                    # "refresh_token": refresh_token
                },
                status=status.HTTP_200_OK
            )

        return Response(
            "User active or Please enter the correct OTP.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["PATCH"])
    def regenerate_otp(self, request, pk=None):
        """
        Regenerate OTP for the given user and send it to the user.
        """
        instance = self.get_object()
        if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
            return Response(
                "Max OTP try reached, try after an hour",
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try) - 1

        instance.otp = otp
        instance.otp_expiry = otp_expiry
        instance.max_otp_try = max_otp_try
        if max_otp_try == 0:
            # Set cool down time
            otp_max_out = timezone.now() + datetime.timedelta(hours=1)
            instance.otp_max_out = otp_max_out
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        else:
            instance.otp_max_out = None
            instance.max_otp_try = max_otp_try
        instance.save()
        send_otp(instance.phone_number, otp)
        return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = ClientUserSerializer(self.user).data

        for k, v in serializer.items():
            data[k] = v

        # you can add your more data with this and return
        # data['first_name'] = self.user.first_name
        # data['last_name'] = self.user.last_name

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        return response

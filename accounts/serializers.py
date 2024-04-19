from datetime import datetime, timedelta
import random
from django.conf import settings
from rest_framework import serializers
from accounts.utils import send_otp

from .models import UserAccount



class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer.

    Used in POST and GET
    """

    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "Password must be longer than {} characters".format(
                settings.MIN_PASSWORD_LENGTH
            )
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "Password must be longer than {} characters".format(
                settings.MIN_PASSWORD_LENGTH
            )
        },
    )

    class Meta:
        model = UserAccount
        fields = (
            "id",
            "phone_number",
            "email",
            "password1",
            "password2"
        )
        read_only_fields = ("id",)

    def validate(self, data):
        """
        Validates if both password are same or not.
        """

        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    

    def create(self, validated_data):
        """
        Create method.

        Used to create the user
        """
        otp = random.randint(1000, 9999)
        otp_expiry = datetime.now() + timedelta(minutes = 10)

        user = UserAccount(
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY
        )
        user.set_password(validated_data["password1"])
        user.save()
        send_otp(validated_data["phone_number"], otp)
        return user

class ClientUserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    # first_name = serializers.SerializerMethodField(read_only=True)
    # last_name = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    # role = serializers.SerializerMethodField(read_only=True)
    # profile_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'phone_number']

    def get_id(self, obj):
        return obj.id
    
    # def get_first_name(self, obj):
    #     clientProfile = ClientProfile.objects.get(userAccount = obj.id)
    #     return clientProfile.first_name
    
    # def get_last_name(self, obj):
    #     clientProfile = ClientProfile.objects.get(userAccount = obj.id)
    #     return clientProfile.last_name
    
    def get_email(self, obj):
        return obj.email
    
    def get_phone_number(self, obj):
        return obj.phone_number
    
    # def get_role(self, obj):
    #     clientProfile = ClientProfile.objects.get(userAccount = obj.id)
    #     return clientProfile.designation

    # def get_profile_image(self, obj):
    #     clientProfile = ClientProfile.objects.get(userAccount = obj.id)
    #     profile_image = clientProfile.profile_image.url

        return profile_image
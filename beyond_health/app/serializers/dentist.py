from rest_framework import serializers

from beyond_health.app.serializers.base import BaseSerializer
from beyond_health.app.serializers.user import UserListSerializer
from beyond_health.db.models import Dentist, User


class DentistListSerializer(BaseSerializer):
    user = UserListSerializer()

    class Meta:
        model = Dentist
        fields = [
            'id',
            'specialization',
            'license_number',
            'user'
        ]


class DentistSerializer(BaseSerializer):
    # non-related Dentist field (pop before create or update)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    mobile_number = serializers.CharField()

    class Meta:
        model = Dentist
        fields = '__all__'

    def validate_email(self, value):
        # For updates, exclude current user
        if self.instance and hasattr(self.instance, 'user'):
            if User.objects.filter(email=value).exclude(pk=self.instance.user.pk).exists():
                raise serializers.ValidationError("User with this email already exists.")
        return value

    def validate_mobile_number(self, value):
        # For updates, exclude current user
        if self.instance and hasattr(self.instance, 'user'):
            if User.objects.filter(mobile_number=value).exclude(pk=self.instance.user.pk).exists():
                raise serializers.ValidationError("User with this mobile number already exists.")
        return value

    def create(self, validated_data):
        # pop all the non-related Dentist fields from the validated_data
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.pop("email")
        mobile_number = validated_data.pop("mobile_number")

        # create User
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
        )

        # create Dentist
        dentist = Dentist.objects.create(
            user=user,
            **validated_data
        )
        return dentist

    def update(self, instance, validated_data):
        # Extract user fields (use get() to handle partial updates)
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        email = validated_data.pop("email", None)
        mobile_number = validated_data.pop("mobile_number", None)

        # --- UPDATE USER ---
        if any([first_name, last_name, email, mobile_number]):
            user = instance.user

            # Update only the fields that were provided
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if email is not None:
                user.email = email
            if mobile_number is not None:
                user.mobile_number = mobile_number

            # Save the user (this will trigger validation)
            user.save()

        # --- UPDATE DENTIST ---
        dentist = super().update(instance, validated_data)
        return dentist

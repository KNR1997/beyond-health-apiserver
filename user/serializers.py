from rest_framework import serializers
from django.db import transaction

from authentication.models import User
from authentication.serializers import UserLiteSerializer
from core.permissions.base import ROLE
from user.models import Patient, Dentist, Staff


class AdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile_number', 'email', 'display_name', 'first_name', 'last_name', 'is_active']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile_number', 'email', 'display_name', 'first_name', 'last_name', 'is_active']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientListSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()

    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'gender'
        ]


class PatientCreateSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ["user"]

    # --- CREATE (TRANSACTIONAL) ---
    @transaction.atomic
    def create(self, validated_data):
        # Extract fields NOT in Student model
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        mobile_number = validated_data.pop("mobile_number")

        # Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            role=ROLE.PATIENT.value,
            mobile_number=mobile_number,
        )
        user.set_password(password)
        user.save()

        # Now validated_data ONLY contains Patient model fields
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


class PatientUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["user"]

    # --- VALIDATION ---
    def validate_username(self, value):
        user = self.instance.user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value

    def validate_email(self, value):
        user = self.instance.user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    # --- UPDATE ---
    def update(self, instance, validated_data):
        """
        instance → Patient instance
        instance.user → related User instance
        validated_data → student fields + username/email/password
        """

        user = instance.user

        # Extract user fields
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        username = validated_data.pop("username", None)
        email = validated_data.pop("email", None)

        # Update User fields
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()

        # Update Patient fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class DentistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentist
        fields = '__all__'


class DentistCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Dentist
        fields = '__all__'
        read_only_fields = ["user"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    # --- CREATE ---
    def create(self, validated_data):
        # Extract fields NOT in Student model
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            role=ROLE.DENTIST.value,
        )
        user.set_password(password)
        user.save()

        # Now validated_data ONLY contains Dentis model fields
        dentist = Dentist.objects.create(user=user, **validated_data)
        return dentist


class DentistUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Dentist
        fields = "__all__"
        read_only_fields = ["user"]

    # --- VALIDATION ---
    def validate_username(self, value):
        user = self.instance.user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value

    def validate_email(self, value):
        user = self.instance.user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    # --- UPDATE ---
    def update(self, instance, validated_data):
        """
        instance → Patient instance
        instance.user → related User instance
        validated_data → student fields + username/email/password
        """

        user = instance.user

        # Extract user fields
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        username = validated_data.pop("username", None)
        email = validated_data.pop("email", None)

        # Update User fields
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()

        # Update Patient fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class DentistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentist
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

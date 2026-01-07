from rest_framework import serializers

from beyond_health.app.serializers.base import BaseSerializer
from beyond_health.db.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'mobile_number',
            'email',
            'display_name',
            'first_name',
            'last_name',
            'is_active',
            'role_name'
        ]


class UserLiteSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'display_name',
            'mobile_number',
            'email',
            'first_name',
            'last_name'
        ]

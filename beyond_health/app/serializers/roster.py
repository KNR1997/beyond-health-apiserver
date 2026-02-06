from rest_framework import serializers

from beyond_health.app.serializers.shift import ShiftListSerializer
from beyond_health.app.serializers.user import UserLiteSerializer
from beyond_health.db.models.roster import RosterWeek, RosterAssignment


class RosterWeekListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RosterWeek
        fields = [
            'id',
            'week_start_date',
            'week_end_date',
            'status',
        ]


class RosterAssignmentListSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()
    shift = ShiftListSerializer()

    class Meta:
        model = RosterAssignment
        fields = [
            'id',
            'roster_week',
            'date',
            'shift',
            'assigned_role',
            'user',
        ]


class RosterAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RosterAssignment
        fields = [
            'roster_week',
            'date',
            'shift',
            'user',
            'assigned_role',
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

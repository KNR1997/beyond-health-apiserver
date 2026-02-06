from rest_framework import serializers

from beyond_health.db.models.roster import RosterWeek


class RosterWeekListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RosterWeek
        fields = [
            'id',
            'week_start_date',
            'week_end_date',
            'status',
        ]

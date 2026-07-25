from rest_framework import serializers
from django.db import transaction
from beyond_health.app.permissions.base import ROLE

from beyond_health.app.serializers.shift import ShiftListSerializer
from beyond_health.app.serializers.user import UserLiteSerializer
from beyond_health.db.models.roster import RosterWeek, RosterAssignment
from beyond_health.db.models.user import User
from beyond_health.db.models.shift import Shift


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


class RosterAssignmentCreateSerializer(serializers.Serializer):
    roster_week = serializers.UUIDField()
    date = serializers.DateField()
    shift = serializers.IntegerField()
    dentist = serializers.UUIDField(required=False, allow_null=True)
    staff = serializers.UUIDField(required=False, allow_null=True)

    def validate(self, attrs):
        # Get or validate roster_week
        try:
            roster_week = RosterWeek.objects.get(id=attrs['roster_week'])
        except RosterWeek.DoesNotExist:
            raise serializers.ValidationError({
                'roster_week': 'Roster week does not exist.'
            })
        attrs['roster_week_instance'] = roster_week

        # Validate shift exists
        try:
            shift = Shift.objects.get(id=attrs['shift'])
        except Shift.DoesNotExist:
            raise serializers.ValidationError({
                'shift': 'Shift does not exist.'
            })
        attrs['shift_instance'] = shift

        # Ensure at least one of dentist or staff is provided
        if not attrs.get('dentist') and not attrs.get('staff'):
            raise serializers.ValidationError(
                "At least one of dentist or staff must be provided."
            )

        # Validate dentist if provided
        dentist_user = None
        if attrs.get('dentist'):
            try:
                dentist_user = User.objects.get(id=attrs['dentist'])
                if dentist_user.role != ROLE.DENTIST.value:
                    raise serializers.ValidationError({
                        'dentist': 'Provided user is not a dentist.'
                    })
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    'dentist': 'Dentist user does not exist.'
                })
        attrs['dentist_user'] = dentist_user

        # Validate staff if provided
        staff_user = None
        if attrs.get('staff'):
            try:
                staff_user = User.objects.get(id=attrs['staff'])
                if staff_user.role != ROLE.STAFF.value:
                    raise serializers.ValidationError({
                        'staff': 'Provided user is not a support staff.'
                    })
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    'staff': 'Staff user does not exist.'
                })
        attrs['staff_user'] = staff_user

        # Check for duplicate assignments (same date, shift, user)
        users_to_check = []
        if dentist_user:
            users_to_check.append(dentist_user)
        if staff_user:
            users_to_check.append(staff_user)

        for user in users_to_check:
            if RosterAssignment.objects.filter(
                date=attrs['date'],
                shift=shift,
                user=user
            ).exists():
                raise serializers.ValidationError({
                    'non_field_errors': f'User {user} is already assigned to this date and shift.'
                })

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        assignments = []

        # Create dentist assignment if provided
        if validated_data.get('dentist_user'):
            print('dentist_assignment')
            dentist_assignment = RosterAssignment(
                roster_week=validated_data['roster_week_instance'],
                date=validated_data['date'],
                shift=validated_data['shift_instance'],
                user=validated_data['dentist_user'],
                assigned_role=ROLE.DENTIST.value,
            )
            # Validate business rules
            dentist_assignment.clean()
            dentist_assignment.save()
            assignments.append(dentist_assignment)

        # Create staff assignment if provided
        if validated_data.get('staff_user'):
            print('staff_assignment')
            staff_assignment = RosterAssignment(
                roster_week=validated_data['roster_week_instance'],
                date=validated_data['date'],
                shift=validated_data['shift_instance'],
                user=validated_data['staff_user'],
                assigned_role=ROLE.STAFF.value,
            )
            # Validate business rules
            staff_assignment.clean()
            staff_assignment.save()
            assignments.append(staff_assignment)

        # Return the first assignment or None if no assignments created
        return assignments[0] if assignments else None

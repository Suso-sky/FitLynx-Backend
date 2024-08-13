from rest_framework import serializers
from .models import Gym, User, Reservation, Penalty, Attendance, ScheduleDay, Membership


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['gym_id', 'name', 'max_capacity']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id','uid', 'username', 'password', 'email', 'is_admin', 'program', 
            'student_code', 'phone', 'photo_url', 'student_code_edited', 
            'program_edited', 'phone_edited'
        )
        extra_kwargs = {'password': {'write_only': True}}

class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer()  
    gym = GymSerializer()

    class Meta:
        model = Reservation
        fields = ['reservation_id', 'user', 'gym', 'date', 'time', 'hours_amount', 'end_time']

class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        fields = '_all_'

class AttendanceSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    gym = GymSerializer()

    class Meta:
        model = Attendance
        fields = ('attendance_id', 'user', 'date', 'time', 'hours_amount', 'gym')

class ScheduleDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleDay
        fields = '_all_'

class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    gym = GymSerializer()

    class Meta:
        model = Membership
        fields = ['membership_id', 'start_date', 'end_date', 'user', 'gym']
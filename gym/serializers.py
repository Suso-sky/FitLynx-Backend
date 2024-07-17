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

    class Meta:
        model = Reservation
        fields = ('reservation_id', 'user', 'date', 'time', 'hours_amount')

class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):

    user = UserSerializer() 

    class Meta:
        model = Attendance
        fields = ('attendance_id', 'user', 'date', 'time', 'hours_amount')

class ScheduleDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleDay
        fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Membership
        fields = ['membership_id', 'start_date', 'end_date', 'user']

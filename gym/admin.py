from django.contrib import admin
from .models import Gym, Admin, User, Reservation, Penalty, Attendance, ScheduleDay, Membership

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('gym_id', 'name', 'max_capacity')
    search_fields = ('name', 'max_capacity')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'program', 'student_code', 'email', 'uid', 'photo_url')
    search_fields = ('username', 'student_code', 'uid', 'photo_url')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin')
    search_fields = ('username', 'email')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'hours_amount', 'end_time', 'reservation_id')
    list_filter = ('user', 'date')
    search_fields = ('user__student_code', 'date')

@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'penalty_id')
    search_fields = ('user__student_code', 'penalty_id')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'hours_amount', 'attendance_id')
    list_filter = ('user', 'date')
    search_fields = ('user__student_code', 'date')

@admin.register(ScheduleDay)
class ScheduleDayAdmin(admin.ModelAdmin):
    list_display = ('day', 'open_time', 'close_time')
    search_fields = ('day',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'membership_id')
    search_fields = ('user__student_code', 'membership_id')

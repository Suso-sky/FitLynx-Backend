from django.contrib import admin
from .models import Gym, User, Reservation, Penalty, Attendance, ScheduleDay, Membership
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('gym_id', 'name', 'max_capacity')
    search_fields = ('name', 'max_capacity')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'program', 'student_code', 'email', 'uid', 'photo_url', 'is_admin')
    search_fields = ('id', 'username', 'student_code', 'uid', 'photo_url', 'email')
    readonly_fields = ('id',)

    # Opcional: Puedes personalizar estos campos según tus necesidades
    filter_horizontal = ()
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('program', 'student_code', 'uid', 'phone', 'photo_url')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_admin', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    ordering = ('email',)

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


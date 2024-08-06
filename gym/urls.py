from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gym.views.gym_view import GymViewSet

from .views.attendance_views import CreateAttendanceView, AttendancesByUserView, CreateAttendanceWithoutReservationView
from .views.auth_views import LoginView, CheckUserView, CreateUserView, ChangePasswordView, PasswordResetRequestView, PasswordResetConfirmView
from .views.schedule_views import GetSchedulesView, UpdateScheduleView
from .views.membership_views import CancelMembershipView, GetMembershipsView, CreateMembershipView
from .views.penalty_views import PenalizeView
from .views.report_views import ReportView
from .views.user_views import GetUsersView, UserViewSet
from .views.reservation_views import CreateReservationView, GetReservationsView, CancelReservationView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'gyms', GymViewSet)

urlpatterns = [
    path('', include(router.urls)),  # DefaultRouter-generated paths for 'users' and 'gyms'
    
    # Custom paths for specific views
    path('Login/', LoginView.as_view(), name='login'),  # Login endpoint
    path('CheckUser/', CheckUserView.as_view(), name='Check User'),  # Check user endpoint
    path('CreateUser/', CreateUserView.as_view(), name='Create User'),  # Create user endpoint
    path('ChangePassword/', ChangePasswordView.as_view(), name='Change Password'),  # Change Password endpoint
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('GetReport/', ReportView.as_view(), name='Report'),  # Get report endpoint
    path('CreateReserve/', CreateReservationView.as_view(), name='Create Reservation'),  # Create reservation endpoint
    path('AttendancesPerUser/', AttendancesByUserView.as_view(), name='Attendances per User'),  # Attendance per user endpoint
    path('GetReserveList/', GetReservationsView.as_view(), name='Reservations'),  # Get reservations endpoint
    path('GetSchedule/', GetSchedulesView.as_view(), name='Schedule'),  # Get schedule endpoint
    path('PenalizeUser/', PenalizeView.as_view(), name='Penalize'),  # Penalize user endpoint
    path('UpdateSchedule/', UpdateScheduleView.as_view(), name='Update Schedule'),  # Update schedule endpoint
    path('CreateAttendance/', CreateAttendanceView.as_view(), name='Create Attendance'),  # Create attendance endpoint
    path('CreateAttnNoReserve/', CreateAttendanceWithoutReservationView.as_view(), name='Create Attendance without Reservation'),  # Create attendance without reservation endpoint
    path('CreateMembership/', CreateMembershipView.as_view(), name='Create Membership'),  # Create membership endpoint
    path('CancelReserve/', CancelReservationView.as_view(), name='Cancel Reservation'),  # Cancel reservation endpoint
    path('GetMemberships/', GetMembershipsView.as_view(), name='Memberships'),  # Get memberships endpoint
    path('CancelMembership/', CancelMembershipView.as_view(), name='Cancel Membership'),  # Cancel membership endpoint
    path('GetUsers/', GetUsersView.as_view(), name='Users'),  # Get users endpoint

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

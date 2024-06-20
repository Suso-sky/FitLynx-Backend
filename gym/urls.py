from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.views_asistencias import CrearAsistenciaView, AsistenciasPorUsuarioView, CreateAsistenciaSinReservaView
from .views.views_auth import LoginView, CheckUserView, CreateUserView
from .views.views_horarios import GetHorariosView, ActualizarHorarioView
from .views.views_membresias import CancelMembresiaView, GetMembresiasView, CreateMembresiaView
from .views.views_penalizaciones import PenalizarView
from .views.views_reporte import ReporteView
from .views.views_usuarios import GetUsersView, UserViewSet
from .views.views_reservas import CreateReservaView, GetReservasView, CancelReservaView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('Login/', LoginView.as_view(), name='login'),
    path('CheckUser/', CheckUserView.as_view(), name='Check User'),
    path('CreateUser/', CreateUserView.as_view(), name='Create User'),
    path('GetReport/', ReporteView.as_view(), name='Reporte'),
    path('CreateReserve/', CreateReservaView.as_view(), name='Crear Reserva'),
    path('AttendancesPerUser/', AsistenciasPorUsuarioView.as_view(), name='Asistencias por Usuario'),
    path('GetReserveList/', GetReservasView.as_view(), name='Reservas'),
    path('GetSchedule/', GetHorariosView.as_view(), name='Horarios'),
    path('PenalizeUser/', PenalizarView.as_view(), name='Penalizar'),
    path('UpdateSchedule/', ActualizarHorarioView.as_view(), name='Actualizar Horario'),
    path('CreateAttendance/', CrearAsistenciaView.as_view(), name='Crear Asistencia'),
    path('CreateAttnNoReserve/', CreateAsistenciaSinReservaView.as_view(), name='Crear Asistencia sin Reserva'),
    path('CreateMembership/', CreateMembresiaView.as_view(), name='Crear Membresía'),
    path('CancelReserve/', CancelReservaView.as_view(), name='Cancelar Reserva'),
    path('GetMemberships/', GetMembresiasView.as_view(), name='Membresias'),
    path('CancelMembership/', CancelMembresiaView.as_view(), name='Cancelar Membresia'),
    path('GetUsers/', GetUsersView.as_view(), name='Usuarios'),
]


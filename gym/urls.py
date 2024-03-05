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
    path('login/', LoginView.as_view(), name='login'),
    path('CheckUser/', CheckUserView.as_view(), name='Check User'),
    path('CreateUser/', CreateUserView.as_view(), name='Create User'),
    path('Reporte/', ReporteView.as_view(), name='Reporte'),
    path('CreateReserva/', CreateReservaView.as_view(), name='Crear Reserva'),
    path('AsistenciasPerUser/', AsistenciasPorUsuarioView.as_view(), name='Asistencias por Usuario'),
    path('GetReservas/', GetReservasView.as_view(), name='Reservas'),
    path('GetHorarios/', GetHorariosView.as_view(), name='Horarios'),
    path('Penalizar/', PenalizarView.as_view(), name='Penalizar'),
    path('ActualizarHorario/', ActualizarHorarioView.as_view(), name='Actualizar Horario'),
    path('CrearAsistencia/', CrearAsistenciaView.as_view(), name='Crear Asistencia'),
    path('CrearAsistenciaSinReserva/', CreateAsistenciaSinReservaView.as_view(), name='Crear Asistencia sin Reserva'),
    path('CreateMembresia/', CreateMembresiaView.as_view(), name='Crear Membresía'),
    path('CancelReserva/', CancelReservaView.as_view(), name='Cancelar Reserva'),
    path('GetMembresias/', GetMembresiasView.as_view(), name='Membresias'),
    path('CancelMembresia/', CancelMembresiaView.as_view(), name='Cancelar Membresia'),
    path('GetUsers/', GetUsersView.as_view(), name='Usuarios'),
]


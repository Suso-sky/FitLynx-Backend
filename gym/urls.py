from django.urls import path
from .views import (
    CreateAsistenciaSinReservaView,
    LoginView,
    CheckUserView,
    CreateUserView,
    ReporteView,
    CreateReservaView,
    AsistenciasPorUsuarioView,
    GetReservasView,
    PenalizarView,
    ActualizarHorarioView,
    CrearAsistenciaView,
    GetHorariosView,
    CreateMembresiaView,
    CancelReservaView,
    GetMembresiasView,
    GetUsersView,
)

urlpatterns = [
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
    path('GetUsers/', GetUsersView.as_view(), name='Usuarios'),
]


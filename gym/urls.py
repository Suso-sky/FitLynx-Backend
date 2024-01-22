from django.urls import path
from .views import (
    LoginView,
    CheckUserView,
    CreateUserView,
    ReporteView,
    CreateReservaView,
    AsistenciasPorUsuarioView,
    GetReservasView,
    PenalizarView,
    ActualizarHorarioView,
    CrearAsistencia,
    GetHorariosView,
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
    path('CrearAsistencia/', CrearAsistencia.as_view(), name='Crear Asistencia'),
]

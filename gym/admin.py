from django.contrib import admin
from .models import Gym, Admin, User, Reserva, Penalizacion, Asistencia, HorarioDia, Membresia

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('gym_id', 'nombre', 'aforo_max')
    search_fields = ('nombre', 'aforo_max')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'programa', 'codigo_estudiantil', 'email', 'uid', 'photo_url')
    search_fields = ('username', 'codigo_estudiantil', 'uid', 'photo_url')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin')
    search_fields = ('username', 'email')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'hora', 'cantidad_horas','hora_fin', 'id_reserva')
    list_filter = ('usuario', 'fecha')
    search_fields = ('usuario__codigo_estudiantil', 'fecha')

@admin.register(Penalizacion)
class PenalizacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_inicio', 'fecha_fin', 'id_penalizacion')
    search_fields = ('usuario__codigo_estudiantil', 'id_penalizacion')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'hora', 'cantidad_horas', 'id_asistencia')
    list_filter = ('usuario', 'fecha')
    search_fields = ('usuario__codigo_estudiantil', 'fecha')

@admin.register(HorarioDia)
class HorarioDiaAdmin(admin.ModelAdmin):
    list_display = ('dia', 'openTime', 'closeTime')
    search_fields = ('dia',)

@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_inicio', 'fecha_fin', 'id_membresia')
    search_fields = ('usuario__codigo_estudiantil', 'id_membresia')


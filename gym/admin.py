from django.contrib import admin
from .models import User, Reserva, Penalizacion, Asistencia, HorarioDia

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'programa', 'codigo_estudiantil', 'email', 'uid')
    search_fields = ('nombre', 'codigo_estudiantil', 'uid')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'hora', 'cantidad_horas', 'id_reserva')
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
    list_display = ('dia', 'hora_apertura', 'hora_cierre')
    search_fields = ('dia',)

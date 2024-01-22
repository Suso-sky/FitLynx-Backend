from rest_framework import serializers
from .models import User, Reserva, Penalizacion, Asistencia, HorarioDia

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'nombre', 'programa', 'codigo_estudiantil', 'email')

class ReservaSerializer(serializers.ModelSerializer):
    
    usuario = UserSerializer()  

    class Meta:
        model = Reserva
        fields = ('id_reserva', 'usuario', 'fecha', 'hora', 'cantidad_horas')

class PenalizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalizacion
        fields = '__all__'

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'

class HorarioDiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioDia
        fields = '__all__'


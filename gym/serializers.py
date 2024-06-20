from rest_framework import serializers
from .models import User, Admin, Reserva, Penalizacion, Asistencia, HorarioDia, Membresia

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uid', 'username', 'password', 'email', 'is_admin', 'programa', 
            'codigo_estudiantil', 'telefono', 'photo_url', 'codigo_estudiantil_editado', 
            'programa_editado', 'telefono_editado'
        )
        extra_kwargs = {'password': {'write_only': True}}

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

    usuario = UserSerializer() 

    class Meta:
        model = Asistencia
        fields = ('id_asistencia', 'usuario', 'fecha', 'hora', 'cantidad_horas')

class HorarioDiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioDia
        fields = '__all__'

class MembresiaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer() 
    class Meta:
        model = Membresia
        fields = ['id_membresia', 'fecha_inicio', 'fecha_fin', 'usuario']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('username', 'password', 'email', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}


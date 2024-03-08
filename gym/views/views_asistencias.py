from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Reserva, Asistencia
from gym.serializers import ReservaSerializer, AsistenciaSerializer
from django.http import JsonResponse
from django.utils import timezone

class AsistenciasPorUsuarioView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener el uid de los parámetros de la URL
            uid = request.query_params.get('uid')

            # Validar si el usuario existe
            usuario = User.objects.get(uid=uid)

            # Obtener las Asistencias del usuario
            asistencias_usuario = Asistencia.objects.filter(usuario=usuario)
            asistencias_serializer = AsistenciaSerializer(asistencias_usuario, many=True)

            # Obtener las Reservas del usuario
            reservas_usuario = Reserva.objects.filter(usuario=usuario)
            reservas_serializer = ReservaSerializer(reservas_usuario, many=True)

            # Usar .data para obtener los datos serializados
            return JsonResponse({'success': True, 'asistencias': asistencias_serializer.data, 'reservas': reservas_serializer.data}) 
        
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CrearAsistenciaView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id_reserva = request.data.get('id_reserva')

            # Obtener la reserva con el id_reserva proporcionado
            reserva = Reserva.objects.get(id_reserva=id_reserva)

            # Crear la asistencia con los datos de la reserva
            asistencia = Asistencia.objects.create(
                usuario=reserva.usuario,
                fecha=reserva.fecha,
                hora=reserva.hora,
                cantidad_horas=reserva.cantidad_horas
            )

            # Eliminar la reserva
            reserva.delete()

            return Response({"success": True, "message": "Asistencia creada."}, status=status.HTTP_201_CREATED)
        
        except Reserva.DoesNotExist:
            return Response({"success": False, "message": "La reserva no existe."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateAsistenciaSinReservaView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener los datos enviados desde el frontend
            user_data = request.data.get('usuario')
            hora = request.data.get('hora')
            cantidad_horas = request.data.get('cantidad_horas')
            fecha = timezone.now().date()  # Utiliza la fecha actual

            try:
                usuario = User.objects.get(uid=user_data['uid'])
            except User.DoesNotExist:
            # Manejar el caso en el que el usuario no existe
                return Response({"success": False, "message": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)
            # Crear la asistencia
            asistencia = Asistencia.objects.create(
                usuario=usuario,
                fecha=fecha,
                hora=hora,
                cantidad_horas=cantidad_horas
            )

            return Response({"success": True, "message": "Asistencia creada sin reserva."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import Reserva, Penalizacion
from datetime import datetime, timedelta

class PenalizarView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            reserva_id = request.data.get('id')
            fecha_inicio = datetime.strptime(request.data.get('fecha'), '%Y-%m-%d')
            fecha_fin = fecha_inicio + timedelta(days=7)
            reserva = Reserva.objects.get(id_reserva=reserva_id)
            usuario = reserva.usuario

            penalizacion = Penalizacion.objects.create(
                    usuario=usuario,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                )
            
            reserva.delete()

            return Response({'success': True, 'message': 'Reserva penalizada y eliminada'}, status=status.HTTP_200_OK)
        
        except Reserva.DoesNotExist:
            return Response({'success': False, 'message': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

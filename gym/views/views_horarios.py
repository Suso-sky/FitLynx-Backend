from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import HorarioDia
from gym.serializers import HorarioDiaSerializer


class GetHorariosView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todos los horarios 
            horarios = HorarioDia.objects.all()
            serializer = HorarioDiaSerializer(horarios, many=True)

            return Response({'success': True, 'horarios': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActualizarHorarioView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.get('schedules', [])

        for schedule_data in data:
            day = schedule_data.get('day')
            closed = schedule_data.get('closed', False)
            open_time = schedule_data.get('openTime')
            close_time = schedule_data.get('closeTime')

            try:
                horario_dia, created = HorarioDia.objects.get_or_create(dia=day)
                horario_dia.closed = closed
                horario_dia.openTime = open_time if not closed else None
                horario_dia.closeTime = close_time if not closed else None
                horario_dia.save()
            except HorarioDia.DoesNotExist:
                return Response({'success': False, 'message': f'El día {day} no es válido.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': True, 'message': 'Horario actualizado correctamente.'}, status=status.HTTP_200_OK)

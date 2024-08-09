from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import ScheduleDay, Gym
from gym.permissions import IsAdminUser
from gym.serializers import ScheduleDaySerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


class GetSchedulesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        gym_id = self.kwargs.get('gym_id')  # Get gym_id from URL parameters

        try:
            # Filter schedules by gym_id if provided
            if gym_id:
                schedules = ScheduleDay.objects.filter(gym_id=gym_id)
            else:
                schedules = ScheduleDay.objects.all()

            serializer = ScheduleDaySerializer(schedules, many=True)
            return Response({'success': True, 'schedules': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateScheduleView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        gym_id = self.kwargs.get('gym_id') 
        gym = Gym.objects.get(pk=gym_id)
        data = request.data.get('updatedSchedule', None)
        
        if not data:
            return Response({'success': False, 'message': 'No hay datos sobre el horario.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for schedule_data in data:
                day = schedule_data.get('day')
                closed = schedule_data.get('closed', False)
                open_time = schedule_data.get('open_time')
                close_time = schedule_data.get('close_time')

                if not day or (not closed and (not open_time or not close_time)):
                    return Response({'success': False, 'message': f'Información erronea en el día {day}.'}, status=status.HTTP_400_BAD_REQUEST)

                
                schedule, _ = ScheduleDay.objects.get_or_create(day=day, gym=gym)
                schedule.closed = closed
                schedule.open_time = open_time if not closed else None
                schedule.close_time = close_time if not closed else None
                schedule.save()

            return Response({'success': True, 'message': 'Horario actualizado.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
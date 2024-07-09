from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import ScheduleDay
from gym.serializers import ScheduleDaySerializer

class GetSchedulesView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve all schedules
            schedules = ScheduleDay.objects.all()
            serializer = ScheduleDaySerializer(schedules, many=True)

            return Response({'success': True, 'schedules': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateScheduleView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.get('updatedSchedule', [])

        for schedule_data in data:
            day = schedule_data.get('day')
            closed = schedule_data.get('closed', False)
            open_time = schedule_data.get('open_time')
            close_time = schedule_data.get('close_time')

            try:
                schedule, _ = ScheduleDay.objects.get_or_create(day=day)
                schedule.closed = closed
                schedule.open_time = open_time if not closed else None
                schedule.close_time = close_time if not closed else None
                schedule.save()
            except ScheduleDay.DoesNotExist:
                return Response({'success': False, 'message': f'El día {day} no es válido.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': True, 'message': 'Horario actualizado.'}, status=status.HTTP_200_OK)

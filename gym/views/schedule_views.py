from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import ScheduleDay
from gym.permissions import IsAdminUser
from gym.serializers import ScheduleDaySerializer

from rest_framework.permissions import IsAuthenticated


class GetSchedulesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve all schedules
            schedules = ScheduleDay.objects.all()
            serializer = ScheduleDaySerializer(schedules, many=True)

            return Response({'success': True, 'schedules': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateScheduleView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data.get('updatedSchedule', None)
        
        if not data:
            return Response({'success': False, 'message': 'No schedule data provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for schedule_data in data:
                day = schedule_data.get('day')
                closed = schedule_data.get('closed', False)
                open_time = schedule_data.get('open_time')
                close_time = schedule_data.get('close_time')

                if not day or (not closed and (not open_time or not close_time)):
                    return Response({'success': False, 'message': f'Invalid data for {day}.'}, status=status.HTTP_400_BAD_REQUEST)

                schedule, _ = ScheduleDay.objects.get_or_create(day=day)
                schedule.closed = closed
                schedule.open_time = open_time if not closed else None
                schedule.close_time = close_time if not closed else None
                schedule.save()

            return Response({'success': True, 'message': 'Updated schedule.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
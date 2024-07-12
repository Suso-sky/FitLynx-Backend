from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import Reservation, Penalty
from datetime import datetime, timedelta

from rest_framework.permissions import IsAuthenticated
from gym.permissions import IsAdminUser

class PenalizeView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            # Obtain data from the POST request
            reservation_id = request.data.get('id')
            start_date = datetime.strptime(request.data.get('date'), '%Y-%m-%d')
            end_date = start_date + timedelta(days=7)
            
            # Retrieve the reservation object
            reservation = Reservation.objects.get(id_reservation=reservation_id)
            user = reservation.user

            # Create a penalty entry for the user
            penalty = Penalty.objects.create(
                user=user,
                start_date=start_date,
                end_date=end_date,
            )
            
            # Delete the reservation after penalizing
            reservation.delete()

            return Response({'success': True, 'message': 'Reservation penalized and deleted'}, status=status.HTTP_200_OK)
        
        except Reservation.DoesNotExist:
            return Response({'success': False, 'message': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

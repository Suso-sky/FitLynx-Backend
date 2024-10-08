from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Reservation, Attendance, Gym
from gym.serializers import ReservationSerializer, AttendanceSerializer
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from gym.permissions import IsAdminUser

class AttendancesByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        gym_id = self.kwargs.get('gym_id')
        uid = request.query_params.get('uid')

        try:
            # Validate if the user exists
            user = User.objects.get(uid=uid)

            
            if gym_id:
                user_attendances = Attendance.objects.filter(user=user, gym_id=gym_id)
                user_reservations = Reservation.objects.filter(user=user, gym_id=gym_id)
            else:
                user_attendances = Attendance.objects.filter(user=user)
                user_reservations = Reservation.objects.filter(user=user)
            
            attendances_serializer = AttendanceSerializer(user_attendances, many=True)
            reservations_serializer = ReservationSerializer(user_reservations, many=True)

            return JsonResponse({'success': True, 'attendances': attendances_serializer.data, 'reservations': reservations_serializer.data})
        
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            reservation_id = request.data.get('reservation_id')

            # Get the reservation with the provided reservation_id
            reservation = Reservation.objects.get(reservation_id=reservation_id)

            # Create the attendance with the reservation data
            Attendance.objects.create(
                user=reservation.user,
                date=reservation.date,
                time=reservation.time,
                hours_amount=reservation.hours_amount,
                gym=reservation.gym
            )

            # Delete the reservation
            reservation.delete()

            return Response({"success": True, "message": "Asistencia confirmada."}, status=status.HTTP_201_CREATED)
        
        except Reservation.DoesNotExist:
            return Response({"success": False, "message": "La reserva no existe."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateAttendanceWithoutReservationView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            # Get the data sent from the frontend
            user_data = request.data.get('user')
            hour = request.data.get('time')
            hours_amount = request.data.get('hours_amount')
            date = timezone.now().date() 
            gym_id = request.data.get('gym_id')
            gym = Gym.objects.get(pk=gym_id)
        
            try:
                user = User.objects.get(uid=user_data['uid'])
            except User.DoesNotExist:
                # Handle the case where the user does not exist
                return Response({"success": False, "message": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)
            # Create the attendance
            Attendance.objects.create(
                user=user,
                date=date,
                time=hour,
                hours_amount=hours_amount,
                gym=gym
            )

            return Response({"success": True, "message": "Asistencia creada."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

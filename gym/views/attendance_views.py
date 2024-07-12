from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Reservation, Attendance
from gym.serializers import ReservationSerializer, AttendanceSerializer
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from gym.permissions import IsAdminUser

class AttendancesByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Get the uid from the URL parameters
            uid = request.query_params.get('uid')

            # Validate if the user exists
            user = User.objects.get(uid=uid)

            # Get the user's Attendances
            user_attendances = Attendance.objects.filter(user=user)
            attendances_serializer = AttendanceSerializer(user_attendances, many=True)

            # Get the user's Reservations
            user_reservations = Reservation.objects.filter(user=user)
            reservations_serializer = ReservationSerializer(user_reservations, many=True)

            # Use .data to get the serialized data
            return JsonResponse({'success': True, 'attendances': attendances_serializer.data, 'reservations': reservations_serializer.data}) 
        
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'The user does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
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
            attendance = Attendance.objects.create(
                user=reservation.user,
                date=reservation.date,
                time=reservation.time,
                hours_amount=reservation.hours_amount
            )

            # Delete the reservation
            reservation.delete()

            return Response({"success": True, "message": "Attendance created."}, status=status.HTTP_201_CREATED)
        
        except Reservation.DoesNotExist:
            return Response({"success": False, "message": "The reservation does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
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
            date = timezone.now().date()  # Use the current date

            try:
                user = User.objects.get(uid=user_data['uid'])
            except User.DoesNotExist:
                # Handle the case where the user does not exist
                return Response({"success": False, "message": "The user does not exist."}, status=status.HTTP_404_NOT_FOUND)
            # Create the attendance
            attendance = Attendance.objects.create(
                usuario=user,
                fecha=date,
                hora=hour,
                cantidad_horas=hours_amount
            )

            return Response({"success": True, "message": "Attendance created without reservation."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

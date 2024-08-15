from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Reservation, Penalty, ScheduleDay, Attendance, Gym, Membership
from gym.serializers import ReservationSerializer
from datetime import datetime, timedelta
import json
from dateutil.relativedelta import relativedelta, MO
from django.db.models import Sum

from rest_framework.permissions import IsAuthenticated

class CreateReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            reservation_date = datetime.strptime(data.get('reservation_date'), '%Y-%m-%d')
            current_date = datetime.strptime(data.get('current_date'), '%Y-%m-%d')
            reservation_time = datetime.strptime(data.get('reservation_time'), '%H:%M').time()
            hours_amount = int(data.get('hours_amount')) 
            user = User.objects.get(uid=uid)
            gym_id = data.get('gym_id')
            gym = Gym.objects.get(pk=gym_id)

            if user.is_admin:
                return Response({"success": False, "message": "Los administradores no pueden realizar reservas."}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                penalty_user = Penalty.objects.get(user=user, gym=gym, end_date__gte=current_date)
                next_day_end = penalty_user.end_date + timedelta(days=1)
                next_day_str = next_day_end.strftime('%Y-%m-%d')
                return Response({"success": False, "message": f"Estás penalizad@ , no puedes hacer una reserva, puedes volver a reservar desde el dia {next_day_str}."}, status=status.HTTP_401_UNAUTHORIZED)
            except Penalty.DoesNotExist:
                pass

            try:
                membership_user = Membership.objects.get(user=user, gym=gym, end_date__gte=current_date)
                
            except Membership.DoesNotExist:
                
                last_monday = current_date + relativedelta(weekday=MO(-1))
                total_attendance_hours = Attendance.objects.filter(
                    user=user,
                    gym=gym,
                    date__gte=last_monday
                ).aggregate(total_hours=Sum('hours_amount'))['total_hours'] or 0
                is_pe_student = str(user.student_code).startswith('14810')

                if (is_pe_student and total_attendance_hours >= 4) or (not is_pe_student and total_attendance_hours >= 2):
                    return Response({
                        "success": False, 
                        "message": "Has alcanzado tu límite semanal de asistencia gratuita, puedes reservar de nuevo la próxima semana o adquirir una memebresía. Para más informacion, acercarse a las instalaciones del gimnasio."
                    }, status=status.HTTP_401_UNAUTHORIZED)

            max_capacity = gym.max_capacity
            start_new_reservation = datetime.combine(reservation_date, reservation_time)
            end_new_reservation = start_new_reservation + timedelta(hours=hours_amount)

            overlapping_reservations = Reservation.objects.filter(
                date=reservation_date,
                time__lte=end_new_reservation,
                end_time__gte=start_new_reservation,
                gym=gym  
            )

            if overlapping_reservations.count() >= max_capacity:
                return Response({"success": False, "message": "Aforo lleno para este intervalo de tiempo."}, status=status.HTTP_401_UNAUTHORIZED)

            user_reservations = Reservation.objects.filter(user=user).exists()
            if user_reservations:
                return Response({"success": False, "message": "Ya has realizado una reserva previamente."}, status=status.HTTP_401_UNAUTHORIZED)

            reservation_date_day = reservation_date.strftime('%A')

            days = { 
                "Monday": "Lunes",
                "Tuesday": "Martes",
                "Wednesday": "Miércoles", 
                "Thursday": "Jueves",
                "Friday": "Viernes",
                "Saturday": "Sábado", 
                "Sunday": "Domingo",
            }
            try:
              #  schedule_day = ScheduleDay.objects.get(day=days[reservation_date_day])
                schedule_day = ScheduleDay.objects.get(day=days[reservation_date_day], gym=gym)
            except ScheduleDay.DoesNotExist:
                return Response({'success': False, 'message': f'El dia {days[reservation_date_day]} no tiene un horario asignado.'}, status=status.HTTP_400_BAD_REQUEST)

            if schedule_day.closed:
                return Response({'success': False, 'message': f'El dia {days[reservation_date_day]} está cerrado el gimnasio.'}, status=status.HTTP_401_UNAUTHORIZED)

            open_datetime = datetime.combine(reservation_date, schedule_day.open_time)
            close_datetime = datetime.combine(reservation_date, schedule_day.close_time)

            if not (open_datetime <= datetime.combine(reservation_date, reservation_time) <= close_datetime and datetime.combine(reservation_date, reservation_time) + timedelta(hours=hours_amount) <= close_datetime):
                return Response({"success": False, "message": "La hora no está dentro del rango permitido."}, status=status.HTTP_401_UNAUTHORIZED)

            Reservation.objects.create(
                user=user,
                date=reservation_date,
                time=reservation_time,
                hours_amount=hours_amount,
                gym=gym
            )

            return Response({"success": True, "message": "Reserva creada exitosamente."}, status=status.HTTP_201_CREATED) 
        
        except User.DoesNotExist:
            return Response({"success": False, "message": "Primero debe rellenar el formulario de registro."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        gym_id = self.kwargs.get('gym_id') 

        try:
            if gym_id:
                reservations = Reservation.objects.filter(gym_id=gym_id)
            else:
                reservations = Reservation.objects.all()
            
            serializer = ReservationSerializer(reservations, many=True)
            return Response({'success': True, 'reservations': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CancelReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        reservation_id = data.get('reservation_id')
        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
            reservation.delete()

            return Response({"success": True, "message": "Reserva cancelada."}, status=status.HTTP_200_OK)
        
        except Reservation.DoesNotExist:
            return Response({"success": False, "message": "La reserva no existe."}, status=status.HTTP_404_NOT_FOUND)

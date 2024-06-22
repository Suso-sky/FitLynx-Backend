from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Reservation, Penalty, ScheduleDay, Attendance, Gym, Membership
from gym.serializers import ReservationSerializer
from datetime import datetime, timedelta
import json
from dateutil.relativedelta import relativedelta, MO
from django.db.models import Sum

class CreateReservationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Obtain data from the request body
            data = json.loads(request.body)
            uid = data.get('uid')
            reservation_date = datetime.strptime(data.get('reservation_date'), '%Y-%m-%d')
            current_date = datetime.strptime(data.get('current_date'), '%Y-%m-%d')
            reservation_time = datetime.strptime(data.get('reservation_time'), '%H:%M').time()
            hours_amount = int(data.get('hours_amount'))
            user = User.objects.get(uid=uid)

            # Validate penalty
            try:
                penalty_user = Penalty.objects.get(user=user, end_date__gte=current_date)
                next_day_end = penalty_user.end_date + timedelta(days=1)
                next_day_str = next_day_end.strftime('%Y-%m-%d')
                return Response({"success": False, "message": f"You are penalized, you cannot make a reservation, you can reserve again from {next_day_str}."}, status=status.HTTP_401_UNAUTHORIZED)
            
            except Penalty.DoesNotExist:
                pass  # No active penalty found

            # Validate Membership
            try:
                membership_user = Membership.objects.get(user=user, end_date__gte=current_date)
                print(f"{user.username} has an active membership until {membership_user.end_date}")                
                
            except Membership.DoesNotExist:
                
                print(f"{user.username} does not have active memberships")                
                last_monday = current_date + relativedelta(weekday=MO(-1))
                # Count total hours attended since last Monday
                total_attendance_hours = Attendance.objects.filter(
                    user=user, 
                    date__gte=last_monday
                ).aggregate(total_hours=Sum('hours_amount'))['total_hours'] or 0
                # Check if the user is a physical education student
                is_pe_student = str(user.student_code).startswith('14810')

                if (is_pe_student and total_attendance_hours >= 4) or (not is_pe_student and total_attendance_hours >= 2):
                    return Response({
                        "success": False, 
                        "message": "You have reached your weekly free attendance limit, you can reserve again next week or purchase a gym membership."
                    }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Validate capacity
            
            max_capacity = Gym.objects.get(name='Unillanos').max_capacity
            
            # Calculate time interval for the new reservation
            start_new_reservation = datetime.combine(reservation_date, reservation_time)
            end_new_reservation = start_new_reservation + timedelta(hours=hours_amount) 
         
            # Check existing overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
                date=reservation_date,
                time__lte=end_new_reservation,
                end_time__gte=start_new_reservation
            )
            
            if overlapping_reservations.count() >= max_capacity:
                return Response({"success": False, "message": "Capacity full for this time interval."}, status=status.HTTP_401_UNAUTHORIZED)

            # Check if user has any active reservation    
            user_reservations = Reservation.objects.filter(user=user).exists()
            if user_reservations:
                return Response({"success": False, "message": "You already have a reservation made."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Validate Schedule

            reservation_date_day = reservation_date.strftime('%A')

            days = { "Monday": "Lunes",
                     "Tuesday": "Martes",
                     "Wednesday": "Miércoles", 
                     "Thursday": "Jueves",
                     "Friday": "Viernes",
                     "Saturday": "Sábado", 
                     "Sunday": "Domingo",
                    }
            try:
                schedule_day = ScheduleDay.objects.get(day=days[reservation_date_day])
            except ScheduleDay.DoesNotExist:
                return Response({'success': False, 'message': f'{days[reservation_date_day]} does not have a defined schedule.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the day is closed
            if  schedule_day.closed:
                return Response({'success': False, 'message': f'{days[reservation_date_day]} the gym is closed.'}, status=status.HTTP_401_UNAUTHORIZED)
            
            open_datetime = datetime.combine(reservation_date, schedule_day.open_time)
            close_datetime = datetime.combine(reservation_date, schedule_day.close_time)

            # Check Attendance Range
            if not (open_datetime <= datetime.combine(reservation_date, reservation_time) <= close_datetime and datetime.combine(reservation_date, reservation_time) + timedelta(hours=hours_amount) <= close_datetime):
                return Response({"success": False, "message": "The time is not within the allowed range."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Create the reservation
            reservation = Reservation.objects.create(
                user=user,
                date=reservation_date,
                time=reservation_time,
                hours_amount=hours_amount
            )

            return Response({"success": True, "message": "Reservation created successfully."}, status=status.HTTP_201_CREATED) 
        
        except User.DoesNotExist:
            return Response({"success": False, "message": "You must fill out the registration form first."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetReservationsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtain all reservations
            reservations = Reservation.objects.all()
            serializer = ReservationSerializer(reservations, many=True)

            return Response({'success': True, 'reservations': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelReservationView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        reservation_id = data.get('reservation_id')
        print(reservation_id)
        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
            reservation.delete()

            return Response({"success": True, "message": "Reservation canceled."}, status=status.HTTP_200_OK)
        
        except Reservation.DoesNotExist:
            return Response({"success": False, "message": "The reservation does not exist."}, status=status.HTTP_404_NOT_FOUND)

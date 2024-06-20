from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Reserva, Penalizacion, HorarioDia, Asistencia, Gym, Membresia
from gym.serializers import ReservaSerializer
from datetime import datetime, timedelta
import json
from dateutil.relativedelta import relativedelta, MO
from django.db.models import Sum


class CreateReservaView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener datos del cuerpo de la solicitud
            data = json.loads(request.body)
            uid = data.get('uid')
            fecha_reserva = datetime.strptime(request.data.get('fecha_reserva'), '%Y-%m-%d')  
            fecha_actual = datetime.strptime(request.data.get('fecha_actual'), '%Y-%m-%d') 
            hora = datetime.strptime(data.get('hora'), '%H:%M').time()  
            cantidad_horas = int(data.get('cantHoras'))
            usuario = User.objects.get(uid=uid)

            
            # Validar penalización
            try:
                penalizacion_usuario = Penalizacion.objects.get(usuario=usuario, fecha_fin__gte=fecha_actual)
                fecha_fin_mas_un_dia = penalizacion_usuario.fecha_fin + timedelta(days=1)
                fecha_fin_str = fecha_fin_mas_un_dia.strftime('%Y-%m-%d')
                # fecha_fin_str = penalizacion_usuario.fecha_fin.strftime('%Y-%m-%d') + timedelta(days=1)
                return Response({"success": False, "message": f"Estás penalizad@, no puedes reservar, puedes volver a reservar el {fecha_fin_str}."}, status=status.HTTP_401_UNAUTHORIZED)
            
            except Penalizacion.DoesNotExist:
                
                print(f"{usuario.username} no tiene penalizaciones activas")
                    
            
            # Validar Programa y Membresía
            try:
                membresia_usuario = Membresia.objects.get(usuario=usuario, fecha_fin__gte = fecha_actual)
                print(f"{usuario.username} tiene una membresía activa hasta el {membresia_usuario.fecha_fin}")                
                
            except Membresia.DoesNotExist:
                
                print(f"{usuario.username} no tiene membresías activas")                
                ultimo_lunes = fecha_actual + relativedelta(weekday=MO(-1))
                # Cuenta el numero total de horas asistidas desde el ultimo lunes
                total_horas_asistencia = Asistencia.objects.filter(
                    usuario=usuario, 
                    fecha__gte=ultimo_lunes
                ).aggregate(total_horas=Sum('cantidad_horas'))['total_horas'] or 0
                # Verifica si el usuario es de educación física
                is_edu_fis = str(usuario.codigo_estudiantil).startswith('14810')

                if (is_edu_fis and total_horas_asistencia >= 4) or (not is_edu_fis and total_horas_asistencia >= 2):
                    return Response({
                        "success": False, 
                        "message": "Ya cumpliste tu límite de asistencias gratuitas semanales, puedes volver a reservar hasta la próxima semana o puedes adquirir una membresía en el gym."
                    }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Validar el aforo
                
            aforo_max = Gym.objects.get(nombre='Unillanos').aforo_max
            #aforo_max = 3
            
              # Calcular el intervalo de tiempo para la nueva reserva
            inicio_nueva_reserva = datetime.combine(fecha_reserva, hora)
            fin_nueva_reserva = inicio_nueva_reserva + timedelta(hours=cantidad_horas) 
         
              # Verificar las reservas existentes que se superponen
            reservas_superpuestas = Reserva.objects.filter(
                fecha=fecha_reserva,
                hora__lte=fin_nueva_reserva,
                hora_fin__gte=inicio_nueva_reserva
            )
            
            if reservas_superpuestas.count() >= aforo_max:
                return Response({"success": False, "message": "Aforo completo para este intervalo de tiempo."}, status=status.HTTP_401_UNAUTHORIZED)

            # Validar si tiene alguna reserva activa    
            
            Reservas_usuario = Reserva.objects.filter(usuario=usuario).exists()
            if Reservas_usuario:
                return Response({"success": False, "message": "Ya tienes una reserva realizada."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Validar Horario

            fecha_reserva_day = fecha_reserva.strftime('%A')

            days = { "Monday": "Lunes",
                     "Tuesday": "Martes",
                     "Wednesday": "Miércoles", 
                     "Thursday": "Jueves",
                     "Friday": "Viernes",
                     "Saturday": "Sábado", 
                     "Sunday": "Domingo",
                    }
            try:
                horario_dia = HorarioDia.objects.get(dia=days[fecha_reserva_day])
            except HorarioDia.DoesNotExist:
                return Response({'success': False, 'message': f'El día {days[fecha_reserva_day]} no tiene un horario definido.'}, status=status.HTTP_400_BAD_REQUEST)

              # Verificar si el dia está cerrado
            if  horario_dia.closed:
                 return Response({'success': False, 'message': f'El día {days[fecha_reserva_day]} está cerrado el gimnasio.'}, status=status.HTTP_401_UNAUTHORIZED)
            
            open_datetime = datetime.combine(fecha_reserva, horario_dia.openTime)
            close_datetime = datetime.combine(fecha_reserva, horario_dia.closeTime)

               # Verificar Rango de asistencia 
            if not (open_datetime <= datetime.combine(fecha_reserva, hora) <= close_datetime and datetime.combine(fecha_reserva, hora) + timedelta(hours=cantidad_horas) <= close_datetime):
                return Response({"success": False, "message": "El horario no está dentro del rango permitido."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Crear la reserva
            reserva = Reserva.objects.create(
                usuario=usuario,
                fecha=fecha_reserva,
                hora=hora,
                cantidad_horas=cantidad_horas
            )

            return Response({"success": True, "message": "Reserva creada con éxito."}, status=status.HTTP_201_CREATED) 
        
        except User.DoesNotExist:
            return Response({"success": False, "message": "Debes llenar el formulario de registro primero."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetReservasView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todas las reservas
            reservas = Reserva.objects.all()
            serializer = ReservaSerializer(reservas, many=True)

            return Response({'success': True, 'reservas': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelReservaView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id_reserva = data.get('id_reserva')
        print(id_reserva)
        try:
            reserva = Reserva.objects.get(id_reserva=id_reserva)
            reserva.delete()

            return Response({"success": True, "message": "Reserva cancelada."}, status=status.HTTP_200_OK)
        
        except Reserva.DoesNotExist:
            return Response({"success": False, "message": "La reserva no existe."}, status=status.HTTP_404_NOT_FOUND)
       
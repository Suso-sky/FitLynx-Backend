from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Reserva, Penalizacion, HorarioDia, Asistencia
from .serializers import ReservaSerializer, AsistenciaSerializer, HorarioDiaSerializer
from django.http import HttpResponse
from django.views import View
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime, time, timedelta, date
from django.http import JsonResponse
import json


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        fixed_username = "admin"
        fixed_password = "1234"

        if username == fixed_username and password == fixed_password:
            
            user_data = {
                "username": fixed_username,
                "password": fixed_password,
            }

            return Response({"success": True, "message": "Login exitoso.", "data": user_data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "Usuario o contraseña incorrectos."}, status=status.HTTP_401_UNAUTHORIZED)
        
class CheckUserView(APIView):
    def post(self, request, *args, **kwargs):
        
        data = json.loads(request.body)
        uid = data.get('uid')

        # Realiza la consulta para verificar la existencia del usuario
        user_exists = User.objects.filter(uid=uid).exists()

        # Puedes devolver una respuesta JSON indicando si el usuario existe o no
        return Response({"user_exists": user_exists})

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        
        # Obtener datos de la solicitud POST
        data = json.loads(request.body)
        uid = data.get('uid')
        nombre = data.get('nombre')
        programa = data.get('programa')
        codigo_estudiantil = data.get('codigo')
        email = data.get('email')

        try:
            # Verificar si el usuario ya existe
            user_existente = User.objects.get(uid=uid)
            return Response({"success": False, 'message': 'El usuario ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # Crear un nuevo usuario
            nuevo_usuario = User.objects.create(
                uid=uid,
                nombre=nombre,
                programa=programa,
                codigo_estudiantil=codigo_estudiantil,
                email=email
            )
            return Response({"success": True, "message": "Usuario creado con éxito."}, status=status.HTTP_201_CREATED)
        
class ReporteView(View):
    def get(self, request, *args, **kwargs):
        # Obtener las asistencias de la base de datos
        asistencias = Asistencia.objects.all()

        # Crear un DataFrame de pandas con los datos de las asistencias
        data = {
            'Nombre': [asistencia.usuario.nombre for asistencia in asistencias],
            'Programa': [asistencia.usuario.programa for asistencia in asistencias],
            'Código Estudiantil': [asistencia.usuario.codigo_estudiantil for asistencia in asistencias],
            'Fecha': [asistencia.fecha.strftime('%Y-%m-%d') if isinstance(asistencia.fecha, date) else asistencia.fecha for asistencia in asistencias],
            'Hora': [asistencia.hora.strftime('%H:%M:%S') if isinstance(asistencia.hora, time) else asistencia.hora for asistencia in asistencias],
            'Cantidad de Horas': [asistencia.cantidad_horas for asistencia in asistencias],
        }

        df = pd.DataFrame(data)

        # Crear un libro de Excel y escribir el DataFrame en una hoja
        wb = Workbook()
        ws = wb.active

        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)

        # Configurar las columnas para un mejor formato
        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width

        # Configurar la respuesta HTTP para la descarga del archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=asistencias.xlsx'
        wb.save(response)

        return response

class CreateReservaView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener datos del cuerpo de la solicitud
            data = json.loads(request.body)
            uid = data.get('uid')
            fecha_reserva = datetime.strptime(request.data.get('fecha_reserva'), '%Y-%m-%d')  
            fecha_actual = datetime.strptime(request.data.get('fecha_actual'), '%Y-%m-%d') 
            hora = datetime.strptime(data.get('hora'), '%H:%M').time()  
            cantidad_horas = data.get('cantHoras')
            usuario = User.objects.get(uid=uid)

            # Validar penalización
            
            penalizaciones = Penalizacion.objects.filter(usuario=usuario)
            
            for penalizacion in penalizaciones:
                fecha_inicio_str = penalizacion.fecha_inicio.strftime('%Y-%m-%d')
                fecha_fin_str = penalizacion.fecha_fin.strftime('%Y-%m-%d')

                if datetime.strptime(fecha_inicio_str, '%Y-%m-%d') <= fecha_actual <= datetime.strptime(fecha_fin_str, '%Y-%m-%d'):
                    return Response({"success": False, "message": f"Estás penalizad@, no puedes reservar, puedes volver a reservar el {fecha_fin_str}."})
            
            # Validar el aforo
                
            aforo_max = 3
            # Calcular el intervalo de tiempo para la nueva reserva
            inicio_nueva_reserva = datetime.combine(fecha_reserva, hora)
            fin_nueva_reserva = inicio_nueva_reserva + timedelta(hours=cantidad_horas)

            # Verificar si hay reservas existentes que se superponen
            reservas_superpuestas = Reserva.objects.filter(
                fecha=fecha_reserva,
                hora__lt=fin_nueva_reserva,
                hora__gte=inicio_nueva_reserva
            )

            # Calcular el aforo ocupado en el intervalo de la nueva reserva
            aforo_ocupado = sum(reserva.cantidad_horas for reserva in reservas_superpuestas)

            # Verificar si el aforo estaría completo después de agregar la nueva reserva
            if aforo_ocupado >= aforo_max:
                return Response({"success": False, "message": "Aforo completo para este intervalo de tiempo."})

           # Verificar si al agregar la nueva reserva, el aforo estaría completo en alguna parte del intervalo
            for reserva in reservas_superpuestas:
                reserva_inicio = datetime.combine(reserva.fecha, reserva.hora)
                reserva_fin = reserva_inicio + timedelta(hours=reserva.cantidad_horas)

                if (
                    inicio_nueva_reserva <= reserva_inicio < fin_nueva_reserva or
                    inicio_nueva_reserva < reserva_fin <= fin_nueva_reserva
                ):
                    return Response({"success": False, "message": "Aforo completo para este intervalo de tiempo."})

            # Validar si tiene alguna reserva activa    

            Reservas_usuario = Reserva.objects.filter(usuario=usuario).exists()
            if Reservas_usuario:
                 return Response({"success": False, "message": "Ya tienes una reserva realizada."})


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
                return Response({'success': False, 'message': f'El día {fecha_reserva_day} no tiene un horario definido.'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar si el dia está cerrado
            if  horario_dia.closed:
                 return Response({'success': False, 'message': f'El día {days[fecha_reserva_day]} está cerrado el gimnasio.'}, status=status.HTTP_400_BAD_REQUEST)
            
            open_datetime = datetime.combine(fecha_reserva, horario_dia.openTime)
            close_datetime = datetime.combine(fecha_reserva, horario_dia.closeTime)

            # Verificar Rango de asistencia 
            if not (open_datetime <= datetime.combine(fecha_reserva, hora) <= close_datetime and datetime.combine(fecha_reserva, hora) + timedelta(hours=cantidad_horas) <= close_datetime):
                return Response({"success": False, "message": "El horario no está dentro del rango permitido."}, status=400)
            
            # Crear la reserva
            reserva = Reserva.objects.create(
                usuario=usuario,
                fecha=fecha_reserva,
                hora=hora,
                cantidad_horas=cantidad_horas
            )

            return Response({"success": True, "message": "Reserva creada con éxito."}) 
        
        except User.DoesNotExist:
            return Response({"success": False, "message": "El usuario no existe."}, status=400)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=500)
       
class AsistenciasPorUsuarioView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener el uid de los parámetros de la URL
            uid = request.query_params.get('uid')

            # Validar si el usuario existe
            usuario = User.objects.get(uid=uid)

            # Obtener las reservas para el usuario
            Asistencias_usuario = Asistencia.objects.filter(usuario=usuario)
            serializer = ReservaSerializer(Asistencias_usuario, many=True)

            return JsonResponse({'success': True, 'reservas': serializer.data})
        
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El usuario no existe.'}, status=400)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

        
class GetReservasView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todas las reservas
            reservas = Reserva.objects.all()
            serializer = ReservaSerializer(reservas, many=True)

            return Response({'success': True, 'reservas': serializer.data})
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

class GetHorariosView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todos los horarios 
            horarios = HorarioDia.objects.all()
            serializer = ReservaSerializer(horarios, many=True)

            return Response({'success': True, 'reservas': serializer.data})
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

class PenalizarView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            reserva_id = request.data.get('id')
            fecha_inicio = datetime.strptime(request.data.get('fecha'), '%Y-%m-%d')
            fecha_fin = fecha_inicio + timedelta(days=7)
            reserva = Reserva.objects.get(id_reserva=reserva_id)
            reserva_uid = reserva.usuario.uid
            usuario = User.objects.get(uid = reserva_uid)

            penalizacion = Penalizacion.objects.create(
                    usuario=usuario,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                )
            
            reserva.delete()

            return Response({'success': True, 'message': 'Reserva penalizada y eliminada'})
        
        except Reserva.DoesNotExist:
            return Response({'success': False, 'message': 'Reserva no encontrada'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

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

        return Response({'success': True, 'message': 'Horario actualizado correctamente.'})

class CrearAsistencia(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id_reserva = request.data.get('id_reserva')

            # Obtener la reserva con el id_reserva proporcionado
            reserva = Reserva.objects.get(id_reserva=id_reserva)

            # Crear la asistencia con los datos de la reserva
            asistencia = Asistencia.objects.create(
                usuario=reserva.usuario,
                fecha=reserva.fecha,
                hora=reserva.hora,
                cantidad_horas=reserva.cantidad_horas
            )

            # Eliminar la reserva
            reserva.delete()

            return Response({"success": True, "message": "Asistencia creada y reserva eliminada correctamente."})
        
        except Reserva.DoesNotExist:
            return Response({"success": False, "message": "La reserva no existe."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
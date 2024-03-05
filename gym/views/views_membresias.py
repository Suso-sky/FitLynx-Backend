from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Membresia
from gym.serializers import MembresiaSerializer
import json

class CreateMembresiaView(APIView):
    def post(self, request, *args, **kwargs):
        
        # Obtener datos de la solicitud POST
        data = json.loads(request.body)
        codigo_estudiantil = data.get('cod_estudiante')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        fecha_actual = data.get('fecha_actual')
        
        try:
            # Verificar si el usuario existe
            usuario = User.objects.get(codigo_estudiantil=codigo_estudiantil)
            try:
                # Verificar si el usuario tiene una membresía activa
                Membresia.objects.get(
                    usuario=usuario, 
                    fecha_fin__gte=fecha_inicio,
                    fecha_inicio__lte=fecha_fin
                    )
                
                return Response({"success": False, "message": f"el usuario con el codigo {codigo_estudiantil} ya tiene una membresía activa."}, status=status.HTTP_401_UNAUTHORIZED)
            
            except Membresia.DoesNotExist:

                Membresia.objects.create(
                usuario=usuario,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                )
                return Response({"success": True, "message": "Membresía creada con éxito."}, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response({"success": False, 'message': f'No existe ningún usuario con el codigo estudiantil {codigo_estudiantil}.'}, status=status.HTTP_400_BAD_REQUEST)
 
class GetMembresiasView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todas las Membresias
            membresias = Membresia.objects.all()
            serializer = MembresiaSerializer(membresias, many=True)

            return Response({'success': True, 'membresias': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CancelMembresiaView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id_membresia = data.get('id_membresia')
        print(id_membresia)
        try:
            membresia = Membresia.objects.get(id_membresia=id_membresia)
            membresia.delete()

            return Response({"success": True, "message": "Membresia cancelada."}, status=status.HTTP_200_OK)
        
        except Membresia.DoesNotExist:
            return Response({"success": False, "message": "La Membresia no existe."}, status=status.HTTP_404_NOT_FOUND)

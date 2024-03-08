from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Admin
from django.http import JsonResponse
import json


class LoginView(APIView):
    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")
        
        try:
            admin = Admin.objects.get(username=username)

            if admin.password == password:
                return Response({"success": True, "message": "Login exitoso."}, status=status.HTTP_200_OK)
            
            else:
                return Response({"success": False, "message": "Usuario o contraseña incorrectos."}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Admin.DoesNotExist:
            
            return Response({"success": False, "message": "Usuario o contraseña incorrectos."}, status=status.HTTP_401_UNAUTHORIZED)
            
class CheckUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            email = data.get('email')

            if email.find("@unillanos.edu.co") <= 0:
                return Response({"success": False, "message": "Solo puedes usar FitLynx con un correo institucional. (Prueba con tu correo de extensión '@unillanos')"}, status=status.HTTP_401_UNAUTHORIZED)

            user_exists = User.objects.filter(uid=uid).exists()

            return Response({"user_exists": user_exists, "message": "El usuario existe"})

        except Exception as e:
            # Captura cualquier excepción y envíala al frontend
            return JsonResponse({'error': 'Se produjo un error en el servidor: ' + str(e)}, status=500)

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        
        # Obtener datos de la solicitud POST
        data = json.loads(request.body)
        uid = data.get('uid')
        nombre = data.get('nombre')
        programa = data.get('programa')
        codigo_estudiantil = data.get('codigo')
        email = data.get('email')

        # Validar correo (ya se esta haciendo tan pronto carga la sesión, se puede dejar aqui si se ve necesario)

        #if email.find("@unillanos.edu.co") <= 0:
        #   return Response({"success": False, "message": "Solo puedes usar FitLynx con un correo institucional."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
        # Verificar si el usuario ya existe
            user_existente = User.objects.get(uid=uid)
            return Response({"success": False, 'message': 'El usuario ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
        # Crear un nuevo usuario
            User.objects.create(
                uid=uid,
                nombre=nombre,
                programa=programa,
                codigo_estudiantil=codigo_estudiantil,
                email=email
            )
            
            return Response({"success": True, "message": "Usuario creado con éxito."}, status=status.HTTP_201_CREATED)
        
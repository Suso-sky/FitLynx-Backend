from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User
from django.http import JsonResponse
import json 
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime, timedelta
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                user_data = {
                    "username": user.username,
                    "email": user.email,
                    "uid": user.uid,
                    "is_admin": user.is_admin,
                    "photo_url": user.photo_url,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
                return Response({"success": True, "message": "Inicio de sesión exitoso.", "data": user_data}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Usuario o contraseña incorrecta."}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"success": False, "message": "Usuario o contraseña incorrecta."}, status=status.HTTP_401_UNAUTHORIZED)
        
class CheckUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            email = data.get('email')

            if not email or "@unillanos.edu.co" not in email:
                return Response({
                    "success": False,
                    "message": "Sólo puedes utilizar FitLynx con un correo institucional. (Prueba con tu email de extensión '@unillanos')."
                }, status=status.HTTP_401_UNAUTHORIZED)

            user_exists = User.objects.filter(uid=uid).exists()
            if User.objects.filter(email=email).exists():
                registered_user = User.objects.get(email=email)
                return Response({
                    "success": False,
                    "message": f"Ya existe una cuenta FitLynx asociada al correo {registered_user.email}"
                }, status=status.HTTP_403_FORBIDDEN)

            return Response({"user_exists": user_exists, "message": "User exists"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)

class CreateUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        uid = data.get('uid')
        name = data.get('username')
        program = data.get('program')
        student_code = data.get('student_code')
        email = data.get('email')
        password = data.get('password')
        user_img = data.get('photo_url')

        encrypted_password = make_password(password)

        try:
            existing_user = User.objects.get(uid=uid)
            return Response({"success": False, 'message': 'El usuario ya ha sido ingresado previamente.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            User.objects.create(
                uid=uid,
                username=name,
                program=program,
                student_code=student_code,
                email=email,
                password=encrypted_password,
                photo_url=user_img
            )
            return Response({"success": True, "message": "Usuario creado correctamente."}, status=status.HTTP_201_CREATED)

class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            user = User.objects.get(uid=uid)
            current_password = data.get("current_password")
            new_password = data.get("new_password")
            confirm_new_password = data.get("confirm_new_password")

            if not user.check_password(current_password):
                return Response({"success": False, "message": "La contraseña actual es incorrecta."}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_new_password:
                return Response({"success": False, "message": "Las nuevas contraseñas no coinciden."}, status=status.HTTP_400_BAD_REQUEST)

            if len(new_password) < 8:
                return Response({"success": False, "message": "La nueva contraseña debe tener al menos 8 caracteres."}, status=status.HTTP_400_BAD_REQUEST)

            user.password = make_password(new_password)
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Contraseña cambiada correctamente.",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Restablecer la contraseña'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'noreply@fitlynx.online', [email])
            return Response({"success": True, "message": "Se ha enviado un correo electrónico con las instrucciones para restablecer la contraseña."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"success": False, "message": "No existe un usuario con ese correo electrónico."}, status=status.HTTP_404_NOT_FOUND)
        
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')

        if new_password != confirm_new_password:
            return Response({"success": False, "message": "Las nuevas contraseñas no coinciden."}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({"success": False, "message": "La nueva contraseña debe tener al menos 8 caracteres."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.password = make_password(new_password)
                user.save()
                return Response({"success": True, "message": "Contraseña restablecida correctamente."}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "El enlace de restablecimiento es inválido."}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"success": False, "message": "El enlace de restablecimiento es inválido."}, status=status.HTTP_400_BAD_REQUEST)

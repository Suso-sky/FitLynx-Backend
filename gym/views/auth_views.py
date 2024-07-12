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
                return Response({"success": True, "message": "Login successful.", "data": user_data}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Incorrect username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"success": False, "message": "Incorrect username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        
class CheckUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            email = data.get('email')

            if not email or "@unillanos.edu.co" not in email:
                return Response({
                    "success": False,
                    "message": "You can only use FitLynx with an institutional email. (Try with your '@unillanos' extension email)"
                }, status=status.HTTP_401_UNAUTHORIZED)

            user_exists = User.objects.filter(uid=uid).exists()
            if User.objects.filter(email=email).exists():
                registered_user = User.objects.get(email=email)
                return Response({
                    "success": False,
                    "message": f"There is already a FitLynx account associated with the email {registered_user.email}"
                }, status=status.HTTP_403_FORBIDDEN)

            return Response({"user_exists": user_exists, "message": "User exists"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        uid = data.get('uid')
        name = data.get('username')
        program = data.get('program')
        student_code = data.get('student_code')
        email = data.get('email')
        password = data.get('password')
        user_img = data.get('photo_url')

        try:
            existing_user = User.objects.get(uid=uid)
            return Response({"success": False, 'message': 'User already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            User.objects.create(
                uid=uid,
                username=name,
                program=program,
                student_code=student_code,
                email=email,
                password=password,
                photo_url=user_img
            )
            return Response({"success": True, "message": "User created successfully."}, status=status.HTTP_201_CREATED)

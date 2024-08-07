from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Membership, Gym
from gym.serializers import MembershipSerializer
import json

from rest_framework.permissions import IsAuthenticated
from gym.permissions import IsAdminUser

class CreateMembershipView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        # Get data from the POST request
        data = json.loads(request.body)
        student_code = data.get('student_code')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        gym_id = data.get('gym_id')
        gym = Gym.objects.get(pk=gym_id)
        
        try:
            # Check if the user exists
            user = User.objects.get(student_code=student_code)
            
            try:
                # Check if the user already has an active membership
                Membership.objects.get(
                    user=user, 
                    end_date__gte=start_date,
                    start_date__lte=end_date,
                    gym=gym
                )
                
                return Response({"success": False, "message": f"El usuario con código {student_code} ya tiene una membresía activa en {gym.name}."}, status=status.HTTP_401_UNAUTHORIZED)
            
            except Membership.DoesNotExist:
                Membership.objects.create(
                    user=user,
                    start_date=start_date,
                    end_date=end_date,
                    gym=gym
                )
                return Response({"success": True, "message": "Membresía creada correctamente."}, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response({"success": False, 'message': f"No existe ningún usuario con el codigo {student_code}."}, status=status.HTTP_400_BAD_REQUEST)

class GetMembershipsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        gym_id = self.kwargs.get('gym_id') 

        try:
            if gym_id:
                memberships = Membership.objects.filter(gym_id=gym_id)
            else:
                memberships = Membership.objects.all()

            serializer = MembershipSerializer(memberships, many=True)
            return Response({'success': True, 'memberships': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelMembershipView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        membership_id = data.get('membership_id')
        
        try:
            membership = Membership.objects.get(membership_id=membership_id)
            membership.delete()

            return Response({"success": True, "message": "Membresía cancelada correctamente."}, status=status.HTTP_200_OK)
        
        except Membership.DoesNotExist:
            return Response({"success": False, "message": "La membresía no existe."}, status=status.HTTP_404_NOT_FOUND)

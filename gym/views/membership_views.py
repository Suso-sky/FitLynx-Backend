from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User, Membership
from gym.serializers import MembershipSerializer
import json

class CreateMembershipView(APIView):
    def post(self, request, *args, **kwargs):
        # Get data from the POST request
        data = json.loads(request.body)
        student_code = data.get('student_code')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        current_date = data.get('current_date')
        
        try:
            # Check if the user exists
            user = User.objects.get(student_code=student_code)
            
            try:
                # Check if the user already has an active membership
                Membership.objects.get(
                    user=user, 
                    end_date__gte=start_date,
                    start_date__lte=end_date
                )
                
                return Response({"success": False, "message": f"The user with student code {student_code} already has an active membership."}, status=status.HTTP_401_UNAUTHORIZED)
            
            except Membership.DoesNotExist:
                # Create a new membership
                Membership.objects.create(
                    user=user,
                    start_date=start_date,
                    end_date=end_date,
                )
                return Response({"success": True, "message": "Membership created successfully."}, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response({"success": False, 'message': f"No user exists with student code {student_code}."}, status=status.HTTP_400_BAD_REQUEST)

class GetMembershipsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Get all memberships
            memberships = Membership.objects.all()
            serializer = MembershipSerializer(memberships, many=True)

            return Response({'success': True, 'memberships': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelMembershipView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        membership_id = data.get('membership_id')
        
        try:
            membership = Membership.objects.get(id_Membership=membership_id)
            membership.delete()

            return Response({"success": True, "message": "Membership canceled."}, status=status.HTTP_200_OK)
        
        except Membership.DoesNotExist:
            return Response({"success": False, "message": "Membership does not exist."}, status=status.HTTP_404_NOT_FOUND)

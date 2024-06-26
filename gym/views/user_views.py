from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User
from gym.serializers import UserSerializer
from rest_framework import viewsets

class GetUsersView(APIView):
    def get(self, request, *args, **kwargs):
        student_code = request.query_params.get('student_code', None)
        try:
            if student_code:
                users = User.objects.filter(student_code=student_code)
            else:
                users = User.objects.all()
            serializer = UserSerializer(users, many=True)

            return Response({'success': True, 'userList': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Perform update
        self.perform_update(serializer)
  
        if 'student_code' in request.data:
            instance.student_code_edited = True
            instance.save(update_fields=['student_code_edited'])
        
        if 'program' in request.data:
             instance.program_edited = True
             instance.save(update_fields=['program_edited'])

        if 'phone' in request.data:
            instance.phone_edited = True
            instance.save(update_fields=['phone_edited'])
        
        return Response(serializer.data)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from gym.models import User
from gym.serializers import UserSerializer
from rest_framework import viewsets

class GetUsersView(APIView):
    def get(self, request, *args, **kwargs):
        codigo_estudiantil = request.query_params.get('cod_estudiante', None)
        try:
            if codigo_estudiantil:
                users = User.objects.filter(codigo_estudiantil=codigo_estudiantil)
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
        
        # Realiza la actualización
        self.perform_update(serializer)
  
        if 'codigo_estudiantil' in request.data:
            instance.codigo_estudiantil_editado = True
            instance.save(update_fields=['codigo_estudiantil_editado'])
        
        if 'programa' in request.data:
             instance.programa_editado = True
             instance.save(update_fields=['programa_editado'])

        if 'telefono' in request.data:
            instance.telefono_editado = True
            instance.save(update_fields=['telefono_editado'])
        
        return Response(serializer.data)
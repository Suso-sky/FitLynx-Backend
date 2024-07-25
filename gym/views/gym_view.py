from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from gym.permissions import IsAdminUser
from gym.models import Gym
from gym.serializers import GymSerializer

class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        gym_id = self.kwargs.get('pk')
        return get_object_or_404(Gym, gym_id=gym_id)

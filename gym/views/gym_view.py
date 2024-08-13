from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from gym.permissions import IsAdminUser
from gym.models import Gym
from gym.serializers import GymSerializer
from rest_framework.permissions import AllowAny

class GymViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    def get_object(self):
        gym_id = self.kwargs.get('pk')
        return get_object_or_404(Gym, gym_id=gym_id)

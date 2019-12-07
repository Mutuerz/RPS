# Django rest
from rest_framework import generics
# Serializers
from player.serializers import CreatePlayerSerializer, ListPlayerSerializer
# Models
from .models import Player


class ListPlayers(generics.ListAPIView):
    serializer_class = ListPlayerSerializer
    queryset = Player.objects.all().order_by("name")


# Models
from player.models import Player
from game.models import Game, Round, WinCondition, Game, Action
# Django Rest
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Serializers
from .serializers import StartGameSerializers, CreateRoundSerializer
from player.serializers import CreatePlayerSerializer, ListPlayerSerializer
# Django
from django.db.transaction import atomic
from django.db.models import Q
from django.utils import timezone


class StartGame(generics.CreateAPIView):
    serializer_class = StartGameSerializers


class StartRound(generics.CreateAPIView):
    serializer_class = CreateRoundSerializer

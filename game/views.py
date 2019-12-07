# Models
from player.models import Player
from game.models import Game, Round, WinCondition, Game, Action
# Django Rest
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Serializers
from .serializers import StartGameSerializers, CreateRoundSerializer, ListGameSerializer
from player.serializers import CreatePlayerSerializer, ListPlayerSerializer
# Django
from django.db.transaction import atomic
from django.db.models import Q
from django.utils import timezone


class StartGame(generics.CreateAPIView):
    serializer_class = StartGameSerializers


class StartRound(generics.CreateAPIView):
    serializer_class = CreateRoundSerializer


class ListGamesWon(generics.ListAPIView):
    serializer_class = ListGameSerializer

    def get_queryset(self):
        data = self.request.data
        # We try to get start and end date
        start_date = data.get('start_date', None)
        # We set current time as default
        end_date = data.get('end_date', timezone.now())

        player = Player.objects.get(id=data["player_id"])

        # ORDER_BY
        # If True we make order as asc
        if data.get('order_direction', True):
            order_dict = {
                'finished_at': 'finished_at',
                'started_at': 'started_at',
                'is_finished': 'is_finished',
            }
        else:
            order_dict = {
                'finished_at': '-finished_at',
                'started_at': '-started_at',
                'is_finished': '-is_finished',
            }

        # Finally we create the queryset
        if start_date is None:
            queryset = Game.objects.filter(winner=player).order_by(
                order_dict.get(data.get('order_title', 'finished_at')))
        else:
            queryset = Game.objects.filter(finished_at__range=(start_date, end_date)).order_by(
                order_dict.get(data.get('order_title', 'finished_at')))

        return queryset

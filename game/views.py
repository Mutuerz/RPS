# Models
from player.models import Player
from game.models import Game, Round, WinCondition, Game, Action
# Django Rest
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Serializers
from .serializers import StartGameSerializers, CreateRoundSerializer, ListGameSerializer, ActionSerializer
# Django
from django.utils import timezone


@api_view(['POST'])
def create(request):
    return Response(data={"": ""}, status=200)
    #Action.objects.create(name="Rock")


class ListActions(generics.ListAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()


class StartGame(generics.CreateAPIView):
    """
    Creates a game of RPS between two players
    """
    serializer_class = StartGameSerializers


class StartRound(generics.CreateAPIView):
    """
    Creates a round of Rock, Paper, Scissors
    """
    serializer_class = CreateRoundSerializer


class ListGamesWon(generics.ListAPIView):
    """
    Lists the games won by a player
    """
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

# Models
from .models import Player
from game.models import Game, Round
# Django Rest
from rest_framework import serializers
# Django
from django.db.models import Q


class PlayerSerializer(serializers.Serializer):
    """
    Validates player's names
    """
    name = serializers.CharField(min_length=3, max_length=50)


class ListPlayerSerializer(serializers.ModelSerializer):
    """
    List player's statistics
    """
    id = serializers.IntegerField(read_only=True)
    games_won = serializers.SerializerMethodField()
    rounds_won = serializers.SerializerMethodField()
    games_played = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'name', 'games_won', 'rounds_won', 'games_played']

    def get_games_won(self, player):
        return Game.objects.filter(winner=player).count()

    def get_rounds_won(self, player):
        return Round.objects.filter(winner=player).count()

    def get_games_played(self, player):
        return Game.objects.filter(Q(player_1=player) | Q(player_2=player)).count()

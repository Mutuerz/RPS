# Models
from .models import Player
from game.models import Game, Round
# Django Rest
from rest_framework import serializers
# Django
from django.db.models import Q


class CreatePlayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=3, max_length=50)

    class Meta:
        model = Player
        fields = ['name']

    def create(self, validated_data):
        player = Player(
            name=validated_data['name'],
        )
        player.save()
        return player


class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=50)


class ListPlayerSerializer(serializers.ModelSerializer):
    games_won = serializers.SerializerMethodField()
    rounds_won = serializers.SerializerMethodField()
    games_played = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['name', 'games_won', 'rounds_won', 'games_played']

    def get_games_won(self, player):
        return Game.objects.filter(winner=player).count()

    def get_rounds_won(self, player):
        return Round.objects.filter(winner=player).count()

    def get_games_played(self, player):
        return Game.objects.filter(Q(player_1=player) | Q(player_2=player)).count()

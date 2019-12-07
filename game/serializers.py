# Models
from game.models import Round, WinCondition, Game
from player.models import Player
# Django Rest
from rest_framework import serializers
# Serializers
from player.serializers import PlayerSerializer
# Django
from django.db.transaction import atomic
from django.db.models import Q
from django.utils import timezone


# Todo: Comment all classes
class ReadRoundSerializer(serializers.ModelSerializer):
    """
    Serializes winner of a round
    """
    winner = PlayerSerializer()

    class Meta:
        model = Round
        fields = ['winner', 'played_at']


class CreateRoundSerializer(serializers.ModelSerializer):
    """
    Allows creation of a round
    """
    is_game_finished = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = Round
        fields = ['game', 'action_1', 'action_2', 'is_game_finished', 'winner', 'score']

    def validate(self, data):
        # Here we get the instance of the game
        game = Game.objects.get(id=data['game'].id)
        if game.is_finished:
            raise serializers.ValidationError("The game is already finished")
        return data

    @atomic
    def create(self, validated_data):
        # First we check if the action_1 won
        try:
            WinCondition.objects.get(killer=validated_data['action_1'], victim=validated_data['action_2'])
        except WinCondition.DoesNotExist:
            # Then we check if action_2 won
            try:
                WinCondition.objects.get(killer=validated_data['action_2'], victim=validated_data['action_1'])
            except WinCondition.DoesNotExist:
                # If there is no winner the field remain null, and because finished date will stopped being null we
                # know that the round was a tie
                winner = None
            else:
                winner = Game.objects.get(id=validated_data['game'].id).player_2
        else:
            winner = Game.objects.get(id=validated_data['game'].id).player_1

        # Here we create the instance of the round
        round = Round(
            # Here we assign the winner
            winner=winner,
            game=validated_data['game'],
            action_1=validated_data['action_1'],
            action_2=validated_data['action_2']
        )
        round.save()

        # Here we check if the amount of round required is
        rounds_amount = Round.objects.filter(game=round.game).exclude(winner=None).count()
        # Todo: Make amount of rounds required dynamic
        if rounds_amount >= 3:
            round.game.is_finished = True
            round.game.finished_at = timezone.now()
            round.game.winner = winner
            round.game.save()

        return round

    def get_is_game_finished(self, obj):
        return obj.game.is_finished

    def get_winner(self, obj):
        return obj.winner.name

    def get_score(self, obj):
        # Player_1 score
        player_1 = Game.objects.get(id=obj.game.id).player_1
        player_1_score = Round.objects.filter(winner=player_1).count()

        # Player_2 score
        player_2 = Game.objects.get(id=obj.game.id).player_2
        player_2_score = Round.objects.filter(winner=player_2).count()

        # Here we get the rounds that has been played
        rounds = Round.objects.filter(game=Game.objects.get(id=obj.game.id)).order_by('played_at')
        serializer = ReadRoundSerializer(rounds, many=True)

        score = {
            "previous_rounds": serializer.data,
            "player_1": {"name": player_1.name, "score": player_1_score},
            "player_2": {"name": player_2.name, "score": player_2_score}
        }
        return score


class StartGameSerializers(serializers.ModelSerializer):
    """
    Allows creation of a game and registering new players
    """
    id = serializers.IntegerField(read_only=True)
    player_1 = PlayerSerializer()
    player_2 = PlayerSerializer()

    class Meta:
        model = Round
        fields = ['id', 'player_1', 'player_2']

    @atomic
    def validate(self, data):
        # First we check if the player_1 exist else we create it
        try:
            player_1 = Player.objects.get(name=data['player_1']['name'])
        except Player.DoesNotExist:
            player_1 = Player.objects.create(name=data['player_1']['name'])
        # Now we check if player_2 exist else we create it
        try:
            player_2 = Player.objects.get(name=data['player_2']['name'])
        except Player.DoesNotExist:
            player_2 = Player.objects.create(name=data['player_2']['name'])

        # Here we check if any of the players has an unfinished game
        if Game.objects.filter(Q(player_1=player_1, is_finished=False) | Q(player_2=player_1)).first() is not None:
            raise serializers.ValidationError(str(player_1.name) + " still has an unfinished game")
        if Game.objects.filter(Q(player_1=player_2, is_finished=False) | Q(player_2=player_2)).first() is not None:
            raise serializers.ValidationError(str(player_2.name) + " still has an unfinished game")

        return data

    def create(self, validated_data):
        player_1 = Player.objects.get(name=validated_data['player_1']['name'])
        player_2 = Player.objects.get(name=validated_data['player_2']['name'])
        # Now we must create the game between the two players
        game = Game(player_1=player_1, player_2=player_2)
        game.save()
        return game


class ListGameSerializer(serializers.ModelSerializer):
    """
    This class allows to validate the requested
    player's id and returns the data about his games
    """
    player_id = serializers.IntegerField(read_only=True)  # The requested player's id
    player_1 = PlayerSerializer(read_only=True)
    player_2 = PlayerSerializer(read_only=True)
    winner = PlayerSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ['player_id', 'player_1', 'player_2', 'winner', 'started_at', 'finished_at']

    def validate(self, data):
        # Here we validate that the requested user exists
        serializers.ValidationError("The requested player does not exist")
        try:
            Player.objects.get(id=data['player_id'])
        except Player.DoesNotExist:
            raise serializers.ValidationError("The requested player does not exist")

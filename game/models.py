from django.db import models
from player.models import Player
from django.utils import timezone


class Game(models.Model):
    objects = models.Manager()

    player_1 = models.ForeignKey('player.Player', on_delete=models.DO_NOTHING, related_name='player_1')
    player_2 = models.ForeignKey('player.Player', on_delete=models.DO_NOTHING, related_name='player_2')
    is_finished = models.BooleanField(default=False)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(default=None, null=True)
    winner = models.ForeignKey('player.Player',
                               on_delete=models.DO_NOTHING, default=None, null=True, related_name='winner')


class Action(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=50)


class Round(models.Model):
    objects = models.Manager()

    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    played_at = models.DateTimeField(default=timezone.now)
    action_1 = models.ForeignKey('game.Action', on_delete=models.DO_NOTHING, related_name='action_1')
    action_2 = models.ForeignKey('game.Action', on_delete=models.DO_NOTHING, related_name='action_2')
    winner = models.ForeignKey('player.Player',
                               on_delete=models.DO_NOTHING, default=None, null=True, related_name='round_winner')


class WinCondition(models.Model):
    objects = models.Manager()

    killer = models.ForeignKey('game.Action', on_delete=models.DO_NOTHING, related_name='killer')
    victim = models.ForeignKey('game.Action', on_delete=models.DO_NOTHING, related_name='victim')

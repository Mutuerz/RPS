from django.db import models
from django.utils import timezone


class Player(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(default=timezone.now)

# Models
from .models import Player
# Django Rest
from rest_framework import serializers


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

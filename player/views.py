# Django rest
from rest_framework import generics
from rest_framework.response import Response
# Serializers
from player.serializers import ListPlayerSerializer
# Models
from .models import Player


class ListPlayers(generics.ListAPIView):
    serializer_class = ListPlayerSerializer

    def get_queryset(self):
        data = self.request.data
        # FILTER_BY: Dictionary with the possible filters
        filter_dict = {
            'name': 'name',
        }
        # ORDER_BY
        # If True we make order as asc
        if data.get('order_direction', True):
            order_dict = {
                'name': 'name',
            }
        else:
            order_dict = {
                'name': '-name',
            }
        # Here we create the filter structure giving the requested filter for insensitive contains
        # i.e. "user__first_name__contains"
        filter_title = str(filter_dict.get(data.get('filter_title', 'name'))) + '__icontains'

        # Finally we create the queryset
        queryset = Player.objects.filter(**{filter_title: data.get('filter_param', "")}).order_by(
            order_dict.get(data.get('order_title', 'name')))

        return queryset


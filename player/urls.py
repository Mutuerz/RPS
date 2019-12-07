# Django
from django.urls import path, include
# Models
from . import views as player_views

urlpatterns = [
    path('list_players/', player_views.ListPlayers.as_view()),
]

from django.urls import path
from . import views as game_views

urlpatterns = [
    path('start_round/', game_views.StartRound.as_view()),
    path('start_game/', game_views.StartGame.as_view()),
    path('list_games/', game_views.ListGamesWon.as_view())
]

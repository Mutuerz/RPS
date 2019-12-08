from django.urls import path
from . import views as game_views

urlpatterns = [
    path('start_game/', game_views.StartGame.as_view(), name='start-game'),
    path('start_round/', game_views.StartRound.as_view(), name='start-round'),
    path('list_games/', game_views.ListGamesWon.as_view(), name='list-games'),
    path('list_actions/', game_views.ListActions.as_view(), name='list-actions'),
]

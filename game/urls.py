from django.urls import path, include
from . import views as game_views


urlpatterns = [
    # TODO: User routers
    path('start_round/', game_views.StartRound.as_view()),
    path('start_game/', game_views.StartGame.as_view())
]

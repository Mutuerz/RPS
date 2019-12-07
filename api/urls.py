from django.urls import path, include

urlpatterns = [
    path('player/', include('player.urls')),
    path('game/', include('game.urls'))
]

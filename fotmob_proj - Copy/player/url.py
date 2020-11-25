from django.urls import path, include
from . import views
urlpatterns = [
    path('play/<slug:Team_id>', views.PlayerInfo, name="player_info"),
   
]
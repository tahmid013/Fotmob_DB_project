from django.urls import path, include
from . import views
urlpatterns = [
    path('/sqaud/<slug:Team_id>', views.SquadInfo, name="squad_infos"),
    path('ch/<slug:coach_id>',views.CoachView,name='coach_info',),
    path('pl/<slug:player_id>',views.PlayerView,name='players_info',)

]
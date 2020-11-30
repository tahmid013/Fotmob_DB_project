from django.urls import path, include
from django.conf.urls import url
from . import views
urlpatterns = [
    
    path('/delete_',views.DeleteView,name='delete'),
    path('/player',views.PlayerDelView , name ='player_d'),
    path('/match_',views.MatchDelView,name='match_d'),
    path('/score_',views.ScoreDelView,name='score_d'),
    path('/team_',views.TeamDelView,name='team_d'),
    path('/coach_',views.CoachDelView,name='coach_d'),
    path('/util/<x>/<y>',views.UtilDelView , name ='util_d')
    
]   
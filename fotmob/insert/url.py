from django.urls import path, include
from django.conf.urls import url
from . import views                 
urlpatterns = [
    
    path('/insert_',views.InsertView,name='insert'),
    path('/player_',views.PlayerInsView,name='player'),
    path('/match_',views.MatchInsView,name='match'),
    path('/score_',views.ScoreInsView,name='scores_ins'),
    path('/red_score_',views.RedCardInsView,name='red_ins'),
    path('/yelllow_score_',views.YellowCardInsView,name='y_ins'),
    path('/team_',views.TeamInsView,name='team'),
    path('/referee_',views.RefereeInsView,name='referee'),
    path('/coach_',views.CoachInsView,name='coach'),
    path('/stadium_',views.StadiumInsView,name='stadium'),
    
    
]   
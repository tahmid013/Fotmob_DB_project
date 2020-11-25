from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.HomepageView, name="index"),
    path('main_/scores/', include('scores.url')),

    path('point_tb/', views.TablePoint, name="table"),
    path('<slug:Team_id>', views.TeamInfo,name="team_info"),
    
    path('main_/player/', include('player.url')),

]
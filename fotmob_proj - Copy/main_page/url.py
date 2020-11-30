from django.urls import path, include
from django.conf.urls import url
from . import views
urlpatterns = [
    path('', views.HomepageView, name="index"),
    path('main_/scores/', include('scores.url')),

    path('point_tb/', views.TablePoint, name="table"),
    path('<slug:Team_id>', views.TeamInfo,name="team_info"),
    path('login/', views.LoginView, name="login"),

    path('main_/player/', include('player.url')),
    path('/admin', include('admin.url')),
    path('/insert_',views.InsertView,name='insert1'),
    
]   
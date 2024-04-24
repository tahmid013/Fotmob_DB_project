from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ScoresView, name="scores"),
    path('by_goals/', views.GoalsView, name="goals"),
    path('by_assists/', views.AssistsView, name="assists"),
    path('by_red/', views.RedView, name="red"),
    path('by_yellow/', views.YellowView, name="yellow"),
]
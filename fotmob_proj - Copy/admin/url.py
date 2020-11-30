from django.urls import path, include
from . import views


urlpatterns = [
    path('/<slug:user>', views.AdminHomeView, name="adminop"),
    path('/insert__dsf', include('insert.url')),
    path('/upda__dsf', include('update.url')),
    path('/del__dsf', include('delete.url')),
]

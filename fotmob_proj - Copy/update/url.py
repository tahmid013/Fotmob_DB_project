from django.urls import path, include
from django.conf.urls import url
from . import views
urlpatterns = [
    
    path('/update_',views.UpdateView,name='update'),
    path('/player/<pl_id>',views.PlView,name='pl_up'),
    path('/match/<m_id>',views.MtView,name='m_up'),
    path('/referee/<r_id>',views.RView,name='r_up'),
    path('/team/<t_id>',views.TView,name='t_up'),
    path('/coach/<c_id>',views.CView,name='c_up'),
    path('/score/<s_id>',views.SView,name='s_up'),
    
]   
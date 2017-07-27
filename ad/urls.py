from django.conf.urls import url 
 
from . import views 

urlpatterns = [
    url(r'^$', views.Get, name="get"),
    url(r'^ajax/', views.AjaxRequest, name="ajax"),
    url(r'^profile/', views.Profile, name="profile"),
]
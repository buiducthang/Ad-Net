from django.conf.urls import url 
 
from . import views 

urlpatterns = [
    url(r'^$', views.Get, name="get"),
    url(r'^ajax/', views.AjaxRequest, name="ajax"),
    url(r'^profile', views.Profile, name="profile"),
    url(r'^thay', views.Profile2, name="profile2"),
    url(r'^check/', views.Check_Reload, name="check")
]
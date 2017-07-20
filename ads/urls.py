from django.conf.urls import url 
 
from . import views 

urlpatterns = [
    url(r'^ads/', views.ad, name="ad_s"),
    url(r'^adsajax/', views.get_ads_by_cate, name="ads"),
]
from django.conf.urls import url 
 
from . import views 

urlpatterns = [
    #url(r'^ecommerce', views.Ecommerce, name="ecommerce"),
    url(r'^signup/', views.SignUp, name="eSignUp"),
    url(r'^signin/', views.SignIn, name="eSignIn"),
    url(r'^goods/', views.Goods, name="eGoods"),
    url(r'^detail/', views.Detail, name="eDetail"),
    # url(r'^ecommerce/SignOut', views.SignOut, name="eSignOut"),
]
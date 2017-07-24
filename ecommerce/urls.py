from django.conf.urls import url 
 
from . import views 

urlpatterns = [
    #url(r'^ecommerce', views.Ecommerce, name="ecommerce"),
    url(r'^$',views.Index, name='eIndex'),
    url(r'^index.html',views.Index, name='eIndex.html'),
    url(r'^signup/', views.SignUp, name="eSignUp"),
    url(r'^signin/', views.SignIn, name="eSignIn"),
    url(r'^goods/', views.Goods, name="eGoods"),
    url(r'^detail/', views.Detail, name="eDetail"),
    url(r'^cookie/', views.cookie, name="cookie"),
    url(r'^about.html', views.About, name='eAbout'),
    url(r'^codes.html', views.Codes, name='eCodes'),
    url(r'^faqs.html', views.Faqs, name='eFaqs'),
    url(r'^icons.html', views.Icons, name='eIcons'),
    url(r'^mail.html', views.Mail, name='eMail'),
    url(r'^products.html', views.Products, name='eProducts'),
    url(r'^products1.html', views.Products1, name='eProducts1'),
    url(r'^products2.html', views.Products2, name='eProducts2'),
    url(r'^single.html', views.Single, name='eSingle'),
    url(r'^setads', views.setAds, name='eSetAds'),
    # url(r'^ecommerce/SignOut', views.SignOut, name="eSignOut"),
]
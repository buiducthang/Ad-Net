from django.conf.urls import url 
 
from . import views 

urlpatterns = [
    #url(r'^ecommerce', views.Ecommerce, name="ecommerce"),
    url(r'^$',views.Index, name='eIndex'),
    url(r'^signup/', views.SignUp, name="eSignUp"),
    url(r'^signin/', views.SignIn, name="eSignIn"),
    url(r'^goods/', views.Goods, name="eGoods"),
    url(r'^detail/', views.Detail, name="eDetail"),
    url(r'^about.html', views.About, name='eAbout'),
    url(r'^care.html', views.Care, name='eCare'),
    url(r'^codes.html', views.Codes, name='eCodes'),
    url(r'^contact.html', views.Contact, name='eContact'),
    url(r'^faqs.html', views.Faqs, name='eFaqs'),
    url(r'^hold.html', views.Hold, name='eHold'),
    url(r'^kitchen.html', views.Kitchen, name='eKitchen'),
    url(r'^login.html', views.Login, name='eLogin'),
    url(r'^offer.html', views.Offer, name='eOffer'),
    url(r'^register.html', views.Register, name='eRegister'),
    url(r'^shipping.html', views.Shipping, name='eShipping'),
    url(r'^single.html', views.Single, name='eSingle'),
    url(r'^terms.html', views.Terms, name='eTerms'),
    url(r'^wishlist.html', views.Wishlist, name='eWishlist'),
    # url(r'^ecommerce/SignOut', views.SignOut, name="eSignOut"),
]
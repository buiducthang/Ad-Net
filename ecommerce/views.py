# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.http import *

import json

def SignUp(request):
    if(request.method == 'POST'):
        username = request.POST['acc']
        password = request.POST['password']
        print username, ' ' , password

        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        #Search username
        search = es.search(index="ad",body={"query": {"match": {'username':username}}})
        print search['hits']['total']
        exist = search['hits']['total']

        if(exist == 0):
            #Create user
            es.index(index="ad", doc_type="ad-net", body={"username":username,"password":password})
        else:
            return HttpResponse("user name is existed")

    return render(request, "ecommerce.html")

def SignIn(request):
    if(request.method == 'POST'):
        username = request.POST['acc']
        password = request.POST['password']
        print username, ' ' , password

        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        #Search user
        search = es.search(index="ad",body={"query": {"match": {'username':username}}})
        user = search['hits']['hits'][0]['_source']['username']
        passs = search['hits']['hits'][0]['_source']['password']
        userid = search['hits']['hits'][0]['_id']
        print username, ' ' , passs
        print userid

        if(user == username and passs == password):
            return HttpResponse('sign in success with userid: '+ userid + ' of username '+ user)
        else:
            return HttpResponse("username or pass is wrong")

    return render(request, "ecommerce.html")

def Goods(request):
    return render(request,"goods.html")

def Detail(request):
    #print "ok1"
    if(request.method == 'GET' and request.is_ajax()):
        print "ok1"
        goods = request.GET.get('goods')
        print "goods: " , goods
        return HttpResponse(goods)

def Index(request):
    return render(request,'index.html')
def About(request):
    return render(request,'about.html')
def Care(request):
    return render(request,'care.html')
def Codes(request):
    return render(request,'codes.html')
def Contact(request):
    return render(request,'contact.html')
def Faqs(request):
    return render(request,'faqs.html')
def Hold(request):
    return render(request,'hold.html')
def Kitchen(request):
    return render(request,'kitchen.html')
def Login(request):
    return render(request,'login.html')
def Offer(request):
    return render(request,'offer.html')
def Register(request):
    return render(request,'register.html')
def Shipping(request):
    return render(request,'shipping.html')
def Single(request):
    return render(request,'Single.html')
def Terms(request):
    return render(request,'terms.html')
def Wishlist(request):
    return render(request,'wishlist.html')
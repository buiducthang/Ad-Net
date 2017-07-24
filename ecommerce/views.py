# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.http import *
from django.template import RequestContext
from django.shortcuts import render_to_response

import json
import ast
import datetime

productsName = []
imgSrcs = []

def SignUp(request):
    if(request.method == 'POST'):
        username = request.POST['acc']
        password = request.POST['password']
        print username, ' ' , password

        es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
        
        #Search username
        search = es.search(index="ad",body={"query": {"match": {'username':username}}})
        print search['hits']['total']
        exist = search['hits']['total']

        if(exist == 0):
            #Create user
            user = es.index(index="ad", doc_type="ad-net", body={"username":username,"password":password})
            userid = user['_id']
            print "userid: ", user['_id']
            #Init categories
            categories_goods = {}
            categories_goods['ao'] = 0
            categories_goods['quan'] = 0
            categories_goods['vay'] = 0

            print categories_goods

            #Init Category of goods
            data = {"userid":userid, "ao": categories_goods['ao'], "quan":categories_goods["quan"], 
                        "vay":categories_goods['vay'],"time":0}
            print data
            es.index(index="ad", doc_type="cate", body=data)
        else:
            return HttpResponse("user name is existed")

    return render(request, "signin.html")

def SignIn(request):
    if(request.method == 'POST'):
        username = request.POST['acc']
        password = request.POST['password']
        print username, ' ' , password

        es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
        
        #Search user
        search = es.search(index="ad",body={"query": {"match": {'username':username}}})
        user = search['hits']['hits'][0]['_source']['username']
        passs = search['hits']['hits'][0]['_source']['password']
        userid = search['hits']['hits'][0]['_id']
        print username, ' ' , passs
        print userid

        if(user == username and passs == password):
            request.session['userid'] = userid
            print request.session['userid']
            # request.session['username'] = user
            # print request.session['username']
            #return HttpResponse('sign in success with userid: '+ userid + ' of username '+ user)
            return HttpResponseRedirect('/ecommerce/goods')
        else:
            data = {"result":0}
            return JsonResponse(data)

    return render(request, "signin.html")

def Goods(request):
    #Date time
    time_current = datetime.datetime.now()
    yesterday = datetime.datetime(2017, 7, 24, 11, 5)
    print yesterday
    print "time now:",time_current,"asd"

    print "time:",((time_current - yesterday).total_seconds())/60.0
    return render(request,"goods.html")

def Detail(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    point = 0

    #Search cate by userid
    print "search"
    search = es.search(index="ad", doc_type="cate", body={"query": {"match": {'userid':request.session['userid']}}})
    source = search['hits']['hits'][0]['_source']
    quan = source['quan']
    vay = source['vay']
    ao = source['ao']
    cateid = search['hits']['hits'][0]['_id']

    print quan, '  ', ao, ' ', vay, ' ', cateid

    if(request.method == 'GET' and request.is_ajax()):
        #Get category of goods
        goods = request.GET.get('goods')

        #Check cate
        if(goods == 'quan'):
            quan = quan + 1
            point = quan
        elif (goods == 'vay'):
            vay = vay + 1
            point = vay
        elif (goods == 'ao'):
            ao = ao + 1
            point = ao
        
        #print request.session['quan'], '  ', request.session['ao'], ' ', request.session['vay'], ' ', request.session['cateid']

        #Update cate point
        point_goods = dict()
        point_goods['ao'] = ao
        point_goods['quan'] = quan
        point_goods['vay'] = vay
        point_goods['userid'] = request.session['userid']

        print point_goods

        #update cate point
        es.update(index='ad', doc_type='cate', id=cateid, body={'doc':point_goods})

        #print update
        rs_update = {"update":0}
        return JsonResponse({goods:point})

#Test cookie
def cookie(request):
    response = render_to_response('index-cookie.html')
    #set cookie
    response.set_cookie('cookie', "http://design-develop.net/wp-content/uploads/2012/05/dd_damask_03.jpg")
    return response

def setAds(request):
    if(request.is_ajax() and request.POST):
        

        base_url = 'ecommerce'
        productName = request.POST.get('productName')
        
        imgSrc = request.POST.get('imgSrc')
        
        url = base_url + '/'+ request.POST.get('url')
        print url

        productsName.append(productName)
        print productsName
        imgSrcs.append(imgSrc)
        print imgSrcs

        response = HttpResponse('Xong!')
        response.set_cookie('product_name',productsName)
        response.set_cookie('img_src', imgSrcs)
        response.set_cookie('url',url)
        return response

def Index(request):
    #Cookie for ad
    imgSrc = request.COOKIES.get('img_src','null')
    productName = request.COOKIES.get('product_name','Chua co quang cao')
    url = request.COOKIES.get('url','Chua co quang cao')

    # print "product name:", ast.literal_eval(productName)[-1]
    # print "img: ", ast.literal_eval(imgSrc)[-1]
    ads = zip('Chua co quang cao','#')
    if(productName != 'Chua co quang cao'):
        list_imgSrc = ast.literal_eval(imgSrc)
        list_productName = ast.literal_eval(productName)

        print "length list imgSrc: " ,len(list_imgSrc)

        print "first: ", list_productName
        if(len(list_imgSrc) > 4 and len(list_productName) > 4):
            list_imgSrc = list_imgSrc[1:]
            list_productName = list_productName[1:]
        
        print "after: ", list_productName
        ads = zip(list_productName,list_imgSrc)

        return render(request,'index.html',{'ads':ads, 'url': url})
    return render(request,'index.html',{'ads':ads, 'url': url})

def About(request):
    return render(request,'about.html')
def Codes(request):
    return render(request,'codes.html')
def Faqs(request):
    return render(request,'faqs.html')
def Icons(request):
    return render(request,'icons.html')
def Mail(request):
    return render(request,'mail.html')
def Products(request):
    return render(request,'products.html')
def Products1(request):
    return render(request,'products1.html')
def Products2(request):
    return render(request,'products2.html')
def Single(request):
    return render(request,'single.html')


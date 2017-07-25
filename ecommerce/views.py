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
    time_current = datetime.datetime.now()
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
            categories_goods['mobile'] = 0
            categories_goods['laptop'] = 0
            categories_goods['toy'] = 0
            categories_goods["time"] = 0
            #Them time can xem lai
            categories_goods["time_mobile"] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
            categories_goods["time_laptop"] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
            categories_goods["time_toy"] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
            categories_goods["userid"] = userid
            
            print categories_goods

            #Init Category of goods
            data = {json.dumps(categories_goods)}
            print data
            #sua cho nay can xem lai
            es.index(index="ad-cate", doc_type="cate", body=categories_goods)
        else:
            return HttpResponse("user name is existed")

    return render(request, "index.html")

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
            return render(request, "index.html")
        else:
            data = {"result":0}
            return JsonResponse(data)

    return render(request, "index.html")

#ham test time can xem lai
def Goods(request):
    #Date time
    time_current = datetime.datetime.now()
    yesterday = datetime.datetime(2017, 7, 24, 11, 5)
    print yesterday
    print "time now:",time_current,"asd"

    print "time:",((time_current - yesterday).total_seconds())/60.0

    #Elastic search init
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    #Search cate by userid
    print "search"
    # search = es.search(index="ad", doc_type="cate", body={"query": {"match": {'userid':'AV14BeMo-Q5w_qrdaia3'}}})
    # source = search['hits']['hits'][0]['_source']
    # time = source['time']
    # time_mobile = source['time_mobile']
    # time_laptop = source['time_laptop']
    # time_toy = source['time_toy']

    time_goods= dict()
    
    # if(time == 0):
    time_goods['toy'] = 0
    time_goods['time_laptop'] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
    #print "time_goods:",time_goods['time_mobile']
    time_goods['time_toy'] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
    time_goods['mobile'] = 0
    time_goods['laptop'] = 0
    time_goods['time'] = 1
    time_goods['userid'] = 'AV14BeMo-Q5w_qrdaia3'
    #print "time_goods:",time_goods
    time_goods['time_mobile'] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
    print "time_goods:",time_goods
        
        #es.delete(index="ad", doc_type="cate", id="AV14BeNP-Q5w_qrdaia4")
    es.index(index='ad', doc_type='cate', body=time_goods)
    
    return render(request,"goods.html")

def Detail(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    point = 0

    #Search cate by userid
    print "search"
    search = es.search(index="ad", doc_type="cate", body={"query": {"match": {'userid':request.session['userid']}}})
    source = search['hits']['hits'][0]['_source']
    laptop = source['laptop']
    toy = source['toy']
    mobile = source['mobile']
    cateid = search['hits']['hits'][0]['_id']

    print laptop, '  ', mobile, ' ', toy, ' ', cateid

    if(request.method == 'GET' and request.is_ajax()):
        #Get category of goods
        goods = request.GET.get('goods')

        #Check cate
        if(goods == 'laptop'):
            laptop = laptop + 1
            point = laptop
        elif (goods == 'toy'):
            toy = toy + 1
            point = toy
        elif (goods == 'mobile'):
            mobile = mobile + 1
            point = mobile
        
        #print request.session['laptop'], '  ', request.session['mobile'], ' ', request.session['toy'], ' ', request.session['cateid']

        #Update cate point
        point_goods = dict()
        point_goods['mobile'] = mobile
        point_goods['laptop'] = laptop
        point_goods['toy'] = toy
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


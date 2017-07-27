# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.http import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from dateutil.parser import parse

import subprocess
import json
import ast
import datetime
import sys
from adnet import Service

productsName = []
imgSrcs = []

def SignUp(request):
    
    if(request.method == 'POST'):
        username = request.POST['acc']
        password = request.POST['password']
        print username, ' ' , password

        if(Service.Check_User(username) == 0):
            #Create user
            Service.Create_User(username,password)
        else:
            return HttpResponse("user name is existed")

    return render(request, "index.html")

def SignIn(request):
    if(request.method == 'POST'):
        username = request.POST['acc']
        password = request.POST['password']
        print username, ' ' , password

        #Search user
        search = Service.Search_User_By_Username(username)
        print search['username']

        if(search['username'] == username and search['password'] == password):
            request.session['userid'] = search['userid']
            print request.session['userid']
            # request.session['username'] = user
            # print request.session['username']
            #return HttpResponse('sign in success with userid: '+ userid + ' of username '+ user)
            return render(request, "index.html")
        else:
            data = {"result":0}
            return JsonResponse(data)

    return render(request, "index.html")

#ham test time da check
def Goods(request):
    time_current = datetime.datetime.now()

    source = Service.Search_Cate_By_UserId('AV18o-v_-Q5w_qrdaib7')
    time = source['time']
    #print "time:", time
    time_mobile = source['time_mobile']
    time_laptop = source['time_laptop']
    time_toy = source['time_toy']

    laptop = source['laptop']
    toy = source['toy']
    mobile = source['mobile']

    print "time chenh lech:",((time_current - parse(time_mobile)).total_seconds())/60.0
    
    list_pointgoods = list()

    if(time == 0):
        list_pointgoods= [0,0,0]
        
        Service.Update_Time_And_PointGoods(list_pointgoods,"AV18o-w9-Q5w_qrdaib8","AV18o-v_-Q5w_qrdaib")
        return render(request,"goods.html")
    if(request.method == 'GET' and request.is_ajax()):
        #Get category of goods
        goods = request.GET.get('goods')

        if(goods == 'laptop'):
            laptop = laptop + 1
            point = laptop
        elif (goods == 'toy'):
            toy = toy + 1
            point = toy
        elif (goods == 'mobile'):
            mobile = mobile + 1
            point = mobile

        list_pointgoods.append(toy)
        list_pointgoods.append(mobile)
        list_pointgoods.append(laptop)
        Service.Update_Time_And_PointGoods(list_pointgoods,"AV18o-w9-Q5w_qrdaib8","AV18o-v_-Q5w_qrdaib")

    return render(request,"goods.html")

def Detail(request):
    #Search cate by userid
    cate = Service.Get_Cate_By_UserId(request.session['userid'])

    print cate['laptop'], '  ', cate['mobile'], ' ', cate['toy'], ' ', cate['cateid']

    list_pointgoods = list()
    # source = Service.Search_Cate_By_UserId(request.session['userid'])
    # time = source['time']
        
    # if(time == 0):
    #     list_pointgoods= [0,0,0]
            
    #     Service.Update_Time_And_PointGoods(list_pointgoods,cateid,request.session['userid'])
    #     return render(request,"goods.html")
    
    if(request.method == 'GET' and request.is_ajax()):
        #Get category of goods
        goods = request.GET.get('goods')

        print "goods:",goods

        laptop = cate['laptop']
        toy = cate['toy']
        mobile = cate['mobile']

        if(goods == 'laptop'):
            laptop = laptop + 1
            point = laptop
        elif (goods == 'toy'):
            toy = toy + 1
            point = toy
        elif (goods == 'mobile'):
            mobile = mobile + 1
            point = mobile

        print "toy point:",toy
        list_pointgoods.append(toy)
        list_pointgoods.append(mobile)
        list_pointgoods.append(laptop)

        print "list_pointgoods:",list_pointgoods

        Service.Update_Time_And_PointGoods(list_pointgoods,cate['cateid'],request.session['userid'])

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
    #Get Mac add

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


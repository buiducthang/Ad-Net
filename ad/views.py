# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from elasticsearch import Elasticsearch
from django.http import *

import json
import ast

from adnet import Service
from django.shortcuts import redirect

def Get(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    ip_mac = Service.Get_IP_MAC(request)
    ip = ip_mac[0]
    mac = ip_mac[1]

    # ads = Service.Get_Ads_By_MacAdd(mac)
    #Search by userid
    #print search
    #if (ads == 0):    
    # ads = zip('Chua co quang cao','#')
        # list_imgSrc = ast.literal_eval(imgSrc)
        # list_productName = ast.literal_eval(productName)

        # print "length list imgSrc: " ,len(list_imgSrc)

        # print "first: ", list_productName
        # if(len(list_imgSrc) > 4 and len(list_productName) > 4):
        #     list_imgSrc = list_imgSrc[1:]
        #     list_productName = list_productName[1:]
        
        # print "after: ", list_productName
        # ads = zip(list_productName,list_imgSrc)
        #print "mac_Add:", mac
    imgSrc = Service.Read_File('/home/thuynv/Desktop/check_new.txt')[0]
        #print "imgSrc:", imgSrc
    return render(request,"display.html",{'mac':mac,'ip':ip,'imgSrc':imgSrc, 'productName':'Chua co quang cao', 'url': 'url'})
    #Get by id
    #get = es.get(index="ad", doc_type="ad-net", id="AV1Wa8w4CM-GrZ83-11I")
    #eventId = get['_id']
    #source = get['_source']
    #print "event id:" , get['_id']
    #print "source: ", type(source)
    # imgSrc = ads['img']
    # productName = ads['title']
    # url = ads['url']
    # cate = ads['cate']

    #UPdate by id
    #es.index(index="ad", doc_type="ad-net", id="AV1Wa8w4CM-GrZ83-11I", body={"userid":13,"quan":1})
    
    #Create
    #es.index(index="ad", doc_type="ad-net", body={"userid":15,"dong ho":2})
    
    #Delete by Id
    #es.delete(index="ad", doc_type="ad-net", id="AV1Y3Q6KxaR1NsDMNVAf")
    # return render(request,"display.html",{'mac':mac,'ip':ip,'imgSrc':imgSrc, 'productName':productName, 'url': url})

def AjaxRequest(request):
    if(request.is_ajax() and request.POST):
        ajaxData = request.POST.get('ajaxdata')
        print ajaxData
    return HttpResponse(json.dumps(ajaxData), content_type='application/json')
def Profile(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    # ip_mac = Service.Get_IP_MAC(request)
    # ip = ip_mac[1]
    # mac = ip_mac[0]

    #test mac
    if (request.GET.get('id') == 'thay'):
        mac = 'd0:a6:37:ec:15:67'
        ip = 'aaa'
        ads = Service.Get_Ads_By_MacAdd(mac)
        imgSrc = ads['img']
        productName = ads['title']
        url = ads['url']
        cate = ads['cate']
        img_profile['img_profile']
    else:
        imgSrc = '#'
        productName = 'Chua co quang cao'
        url = 'Chua co quang cao'
        cate = 'Chua co quang cao'
        mac = 'NULL'
        ip = 'NULL'
        img_profile = '#'
    return render(request,"display2.html",{'mac':mac,'ip':ip,'imgSrc':imgSrc, 'productName':productName, 'url': url, 'img_profile': img_profile})
def Profile2(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    # ip_mac = Service.Get_IP_MAC(request)
    # ip = ip_mac[1]
    # mac = ip_mac[0]

    #test ma
    mac = 'd0:a6:37:ec:15:67'
    ip = 'aaa'
    ads = Service.Get_Ads_By_MacAdd(mac)
    if (ads != 0):
        imgSrc = ads['img']
        productName = ads['title']
        url = ads['url']
        cate = ads['cate']
        img_profile = ads['img_profile']
    else:
        imgSrc = 'IMG_SRC'
        productName = 'PRODUCTNAME'
        url = "URL"
        cate = "CATE"
        img_profile = 'IMG PROFILE'

    return render(request,"display2.html",{'mac':mac,'ip':ip,'imgSrc':imgSrc, 'img_profile': img_profile, 'productName':productName, 'url': url, 'img_profile': img_profile})

def Check_Reload(request):
    #check = 'false'

    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    search = es.search(index="ad", doc_type="check", body={"query": {"match": {'check':'false'}}})

    check = search['hits']['total']
    print "check:",check
    if(request.is_ajax() and request.POST):
        ajaxData = request.POST.get('ajaxdata')
        print ajaxData
        if(check != 0):
            reload = 'none'
        else:
            reload = 'reload'    
    return HttpResponse(json.dumps({'result':reload}), content_type='application/json')

def Create_Profile(request):
    if(request.method == 'POST'):
        print "POST"
        img_link = request.POST['link-img']
        mac = request.POST['mac-id']

        print "img_link:",img_link
        print "mac:",mac

        Service.Create_User("username","password",mac,img_link)
        return redirect('profile')

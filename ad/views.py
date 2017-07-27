# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from elasticsearch import Elasticsearch
from django.http import *

import json
import ast

from adnet import Service

def Get(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    ip_mac = Service.Get_IP_MAC(request)
    ip = ip_mac[1]
    mac = ip_mac[0]
    print 'mac: ',mac
    
    #Search by userid
    search = es.search(index="ad",body={"query": {"match": {'userid':'13'}}})
    #print search
    
    imgSrc = request.COOKIES.get('img_src','null')
    productName = request.COOKIES.get('product_name','Chua co quang cao')
    url = request.COOKIES.get('url','Chua co quang cao')
    
    # ads = zip('Chua co quang cao','#')
    print 'productName: ', imgSrc
    if(productName != 'Chua co quang cao'):
        # list_imgSrc = ast.literal_eval(imgSrc)
        # list_productName = ast.literal_eval(productName)

        # print "length list imgSrc: " ,len(list_imgSrc)

        # print "first: ", list_productName
        # if(len(list_imgSrc) > 4 and len(list_productName) > 4):
        #     list_imgSrc = list_imgSrc[1:]
        #     list_productName = list_productName[1:]
        
        # print "after: ", list_productName
        # ads = zip(list_productName,list_imgSrc)

        mac_add = Service.Get_IP_MAC()
        print "mac_Add: ", mac_add[1]
        return render(request,"display.html",{'mac':mac,'ip':ip,'imgSrc':imgSrc, 'productName':productName, 'url': url})
    #Get by id
    #get = es.get(index="ad", doc_type="ad-net", id="AV1Wa8w4CM-GrZ83-11I")
    #eventId = get['_id']
    #source = get['_source']
    #print "event id:" , get['_id']
    #print "source: ", type(source)

    #UPdate by id
    #es.index(index="ad", doc_type="ad-net", id="AV1Wa8w4CM-GrZ83-11I", body={"userid":13,"quan":1})
    
    #Create
    #es.index(index="ad", doc_type="ad-net", body={"userid":15,"dong ho":2})
    
    #Delete by Id
    #es.delete(index="ad", doc_type="ad-net", id="AV1Y3Q6KxaR1NsDMNVAf")

    
    return render(request,"display.html",{'mac':mac,'ip':ip,'imgSrc':imgSrc, 'productName':productName, 'url': url})

def AjaxRequest(request):
    if(request.is_ajax() and request.POST):
        ajaxData = request.POST.get('ajaxdata')
        print ajaxData
    return HttpResponse(json.dumps(ajaxData), content_type='application/json')
def Profile(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    ip_mac = Service.Get_IP_MAC(request)
    ip = ip_mac[1]
    mac = ip_mac[0]

    ads = Service.Get_Ads_By_MacAdd(mac)
    imgSrc = ads['img']
    productName = ads['title']
    url = ads['url']
    cate = ads['cate']
    return render(request,"display2.html",{'mac':mac,'ip':ip,'imgSrc':imgSrc, 'productName':productName, 'url': url})

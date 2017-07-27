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

    ip_mac = Service.Get_IP_MAC(request)
    ip = ip_mac[1]
    mac = ip_mac[0]

    ads = Service.Get_Ads_By_MacAdd(mac)
    imgSrc = ads['img']
    productName = ads['title']
    url = ads['url']
    cate = ads['cate']
    return render(request,"display2.html",{'mac':mac,'ip':ip,'imgSrc':imgSrc, 'productName':productName, 'url': url})

def Create_Profile(request):
    if(request.method == 'POST'):
        print "POST"
        img_link = request.POST['link-img']
        mac = request.POST['mac-id']

        print "img_link:",img_link
        print "mac:",mac

        Service.Create_User("username","password",mac,img_link)
        return redirect('profile')
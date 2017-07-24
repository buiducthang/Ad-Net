# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from elasticsearch import Elasticsearch
from django.http import *

import json
import ast

def Get(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    #Search by userid
    search = es.search(index="ad",body={"query": {"match": {'userid':'13'}}})
    #print search
    
    imgSrc = request.COOKIES.get('img_src','null')
    productName = request.COOKIES.get('product_name','Chua co quang cao')
    url = request.COOKIES.get('url','Chua co quang cao')
    
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

    return render(request,"ad.html",{'imgSrc':list_imgSrc[-1], 'productName':list_productName[-1], 'url': url})

def AjaxRequest(request):
    if(request.is_ajax() and request.POST):
        ajaxData = request.POST.get('ajaxdata')
        print ajaxData
    return HttpResponse(json.dumps(ajaxData), content_type='application/json')
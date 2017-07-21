# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from elasticsearch import Elasticsearch
from django.http import *

import json

def Get(request):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    #Search by userid
    search = es.search(index="ad",body={"query": {"match": {'userid':'13'}}})
    #print search
    imgSrc = request.COOKIES['img_src']
    productName = request.COOKIES['product_name']
    url = request.COOKIES['url']
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

    return render(request,"ad.html",{'imgSrc':imgSrc, 'productName':productName, 'url': url})

def AjaxRequest(request):
    if(request.is_ajax() and request.POST):
        ajaxData = request.POST.get('ajaxdata')
        print ajaxData
    return HttpResponse(json.dumps(ajaxData), content_type='application/json')
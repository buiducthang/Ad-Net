# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from elasticsearch import Elasticsearch
from django.http import *

import json
import operator
import random

def ad(request):
    #test cookie
    #get cookie
    print "cookie: ", request.COOKIES['cookie'] 
    return render(request,"test.html")

def get_ads_by_cate(request):
    print "asdf"
    if(request.is_ajax() and request.POST):
        print "ajax"
        userid = request.POST.get('userid')
        
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        #Search cate by userid
        search = es.search(index="ad", doc_type="cate", body={"query": {"match": {'userid':userid}}})
        source = search['hits']['hits'][0]['_source']

        cate_max = dict()
        cate_max['quan'] = source['quan']
        cate_max['ao'] = source['ao']
        cate_max['vay'] = source['vay']

        #return key of cate_max with max value
        key_max = max(cate_max.iteritems(), key=operator.itemgetter(1))[0]
        print key_max
        

        #Get ads by cate
        print "search rs:"
        #filter_path=['hits.hits._source'] only takes _source
        search_cate = es.search(index="ad", doc_type="ads", body={"query": {"match": {'cate':"quan"}}}, filter_path=['hits.hits._source'])
        
        
        cate_rs_list = search_cate['hits']['hits']
        length_cate_rs_list = len(cate_rs_list)

        #index by random
        index_of_cate_rs_list = random.randint(0,length_cate_rs_list - 1)
        print index_of_cate_rs_list

        cate_rs = search_cate['hits']['hits'][index_of_cate_rs_list]['_source']

        title = cate_rs['tittle']
        link = cate_rs['link']
        point = cate_rs['point']
        
        print title
        response = {"result":title}
        return JsonResponse(response)
    #return render(request,"test.html")
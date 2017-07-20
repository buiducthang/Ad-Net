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
            data = {"userid":userid, "ao": categories_goods['ao'], "quan":categories_goods["quan"], "vay":categories_goods['vay']}
            print data
            es.index(index="ad", doc_type="cate", body=data)
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
            request.session['userid'] = userid
            print request.session['userid']
            # request.session['username'] = user
            # print request.session['username']
            #return HttpResponse('sign in success with userid: '+ userid + ' of username '+ user)
            return HttpResponseRedirect('/ecommerce/goods')
        else:
            data = {"result":0}
            return JsonResponse(data)

    return render(request, "ecommerce.html")

def Goods(request):
    return render(request,"goods.html")

def Detail(request):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

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
        #Get category og goods
        goods = request.GET.get('goods')

        #Check cate
        if(goods == 'quan'):
            quan = quan + 1
        elif (goods == 'vay'):
            vay = vay + 1
        elif (goods == 'ao'):
            ao = ao + 1
        
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
        return HttpResponse(goods)
#Tinh tgian chenh lech tra ve minute
def Time(time_current, time2_string):
    return ((time_current - parse(time2_string)).total_seconds())/60.0

#init time and cate
def Create_User():
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
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
    #da check
    es.index(index="ad", doc_type="cate", body=categories_goods)


#Return Username, password, userid
def Search_User_By_Username(username):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])
    search = es.search(index="ad",body={"query": {"match": {'username':username}}})
    user = search['hits']['hits'][0]['_source']['username']
    passs = search['hits']['hits'][0]['_source']['password']
    userid = search['hits']['hits'][0]['_id']
    print username, ' ' , passs
    print userid
    return (username, passs, userid)

#Update time and point goods
def Update_Time_And_PointGoods(list_pointgoods, cateid, userid, time_current):
    es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

    time_goods= dict()

    time_goods['toy'] = list_pointgoods[0]
    time_goods['time_laptop'] = time_current
    #print "time_goods:",time_goods['time_mobile']
    time_goods['time_toy'] = time_current
    time_goods['mobile'] = list_pointgoods[1]
    time_goods['laptop'] = list_pointgoods[2]
    time_goods['time'] = 1
    time_goods['userid'] = userid
    #print "time_goods:",time_goods
    time_goods['time_mobile'] = time_current
    print "time_goods:",time_goods
            
    es.update(index="ad", doc_type="cate", id=cateid, body={'doc':time_goods})

def get_ads_by_cate(cate):
    #Get ads by cate
    print "search rs:"
    #filter_path=['hits.hits._source'] only takes _source
    search_cate = es.search(index="ad", doc_type="ads", body={"query": {"match": {'cate':cate}}}, filter_path=['hits.hits._source'])
        
        
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
    return title

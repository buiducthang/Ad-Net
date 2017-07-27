from elasticsearch import Elasticsearch
import datetime
import random
import operator
import subprocess

#Init variable
time_current = datetime.datetime.now()
es = Elasticsearch([{'host': '10.12.11.161', 'port': 9200}])

#Check User by username
#If not exist return 0
def Check_User(username):
    print 'username'
    
    search = es.search(index="ad", doc_type="ad-net", body={"query": {"match": {'username':username}}})
    print search['hits']['total']
    exist = search['hits']['total']
    return exist
#Search Cate By Userid return source
def Search_Cate_By_UserId(userid):
    search = es.search(index="ad", doc_type="cate", body={"query": {"match": {'userid':'AV18o-v_-Q5w_qrdaib7'}}})
    source = search['hits']['hits'][0]['_source']
    return source

#Tinh tgian chenh lech tra ve minute
def Time(time_current, time2_string):
    return ((time_current - parse(time2_string)).total_seconds())/60.0

#init time and cate
def Create_User(username, password, macadd):

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
    #Init Time
    categories_goods["time_mobile"] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
    categories_goods["time_laptop"] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
    categories_goods["time_toy"] = time_current.strftime("%Y-%m-%d %H:%M:%S").replace(" ","T")
    categories_goods["userid"] = userid
    
    categories_goods['macadd'] = macadd

    print categories_goods

    es.index(index="ad", doc_type="cate", body=categories_goods)


#Return Username, password, userid
def Search_User_By_Username(username):
    
    search = es.search(index="ad",body={"query": {"match": {'username':username}}})
    user = search['hits']['hits'][0]['_source']['username']
    passs = search['hits']['hits'][0]['_source']['password']
    userid = search['hits']['hits'][0]['_id']
    print username, ' ' , passs
    print userid
    data = {"username":username, "password":passs, "userid":userid}
    return data

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

#Get Ads By Cate Name if not return 0
def Get_Ads_By_Cate(cate):
    #Get ads by cate
    print "search rs:"
    #filter_path=['hits.hits._source'] only takes _source
    search_cate = es.search(index="ad", doc_type="ads", body={"query": {"match": {'cate':cate}}}, filter_path=['hits.hits._source'])
    print "search_Cate:",search_cate

    if (not search_cate):
         return 0    
    
    cate_rs_list = search_cate['hits']['hits']
    length_cate_rs_list = len(cate_rs_list)

    #index by random
    index_of_cate_rs_list = random.randint(0,length_cate_rs_list - 1)
    print index_of_cate_rs_list

    cate_rs = search_cate['hits']['hits'][index_of_cate_rs_list]['_source']

    title = cate_rs['title']
    link = cate_rs['link']
    point = cate_rs['point']
    cate = cate_rs['cate']

    print title
    data = {"title":title, "link":link, "point":point, "cate":cate}
    return data


#Get cate by userid
def Get_Cate_By_UserId(userid):
    search = es.search(index="ad", doc_type="cate", body={"query": {"match": {'userid':userid}}})
    source = search['hits']['hits'][0]['_source']
    
    cate = dict()
    cate['mobile'] = source['mobile']
    cate['laptop'] = source['laptop']
    cate['toy'] = source['toy']
    cate['cateid'] = search['hits']['hits'][0]['_id']
    return cate

#Get Cate max point by userid
def Get_Cate_Max(dict_cate):
    key_max = max(dict_cate.iteritems(), key=operator.itemgetter(1))[0]
    return key_max

#Get MAC address
def Get_IP_MAC(request):
    x_f = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_f:
        ip = x_f.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    a = subprocess.call(["ping",ip,"-c","1"])
    mac_add = subprocess.Popen(["arp","-a",ip], stdout=subprocess.PIPE)
    out, err = mac_add.communicate()
    return [ip,out.split(" ")[3]]

#Create Ads
def Create_Ads(mac_add, cate_name, title, link_img, url):
    data = {"mac":mac_add, "cate":cate_name, "title":title, "img":link_img, "url":url}
    user = es.index(index="ad", doc_type="advertise", body=data)

#Get Ad By Macadd
def Get_Ads_By_MacAdd(mac_add):
    search = es.search(index="ad", doc_type="advertise", body={"query": {"match": {'mac':mac_add}}})
    #print search['hits']['hits'][0]['_source']
    rs = search['hits']['hits'][0]['_source']
    #print type(rs)
    return rs

#Delete Ads
def Delete_Ads(id_ads):
    dele = es.delete(index="ad", doc_type="advertise", id=id_ads)
    #print dele['result']
    return dele['result']

#Get Id Ad but not return 0
def Get_Ads_Id(mac_add):
    search = es.search(index="ad", doc_type="advertise", body={"query": {"match": {'mac':mac_add}}})
    check = search['hits']['total']
    if check == 0:
        return 0
    rs = search['hits']['hits'][0]['_id']
    return rs

if __name__ == "__main__":
    # ads = Get_Ads_By_Cate('laptop')
    # print ads
    # cate = Get_Cate_By_UserId('AV18o-v_-Q5w_qrdaib')
    # print Get_Cate_Max(cate)
    # ads = Get_Ads_By_MacAdd("456")
    # print ads["title"]
    a = Get_Ads_Id("456")
    print a
    #Delete_Ads(a)

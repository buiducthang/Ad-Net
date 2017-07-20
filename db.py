from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.index(index="ad", doc_type="ad-net", body={"username":"test","password":"test"})

if es.indices.exists(index="a"):
    print "exist"
else:
    print "not"
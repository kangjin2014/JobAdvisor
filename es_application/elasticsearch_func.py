from datetime import datetime
from elasticsearch import Elasticsearch

def es_write(title, company, description, job_id):
    
    es = Elasticsearch()
    
    doc = {'title': title,'company': company,'description': description,'id':job_id}
    
    es.index(index = "job_id", 
             doc_type = 'text',
             id = job_id,
             body = doc)
    
    print (es.get(index = "job_id", 
                  doc_type = 'text',
                  id = job_id))

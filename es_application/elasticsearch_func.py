from datetime import datetime
from elasticsearch import Elasticsearch

def es_write(title, company, description, job_id):
    
    es = Elasticsearch()
    
    doc = {'title': title,'company': company,'description': description,'id':job_id}
    
    es.index(index = "job", 
             doc_type = 'text',
             id = job_id,
             body = doc)
    
    print (es.get(index = "job", 
                  doc_type = 'text',
                  id = job_id))

    print ('Check the url at localhost:9200/job/text/{}'.format(job_id))

def es_match( job_title, keyword):
 
    es = Elasticsearch()

    res = es.search(index='job', body=
    {
      "query": {
        "bool": {
          "should": [
            {
              "match": {
                "title": job_title
              }
            },
            {
              "match": {
                "description": keyword
              }
            }
          ]
        }
      }
    })

    # or following                
    # {
    #   'query': {
    #     'match': {
    #       'description': 'python, data science, data engineering, machine learning'
    #      }
    #   }
    # })
    return res
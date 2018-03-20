from . import elasticsearch_func as ef
def init():
    ef.es_write(title = 'ds', 
                company = 'rbc', 
                description = 'handsome', 
                job_id = '10')

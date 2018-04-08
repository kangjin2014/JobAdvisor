from es_application import elasticsearch_func as ef
from . import job_scraper as js
import numpy as np

def init(kw_title, kw_location, kw_province):
    
    url_int = js.get_frontpage_url(kw_title, kw_location, kw_province)
    
    soup_int = js.soupify(url_int)

    num_jobs, num_pages, current_time = js.get_job_nums(soup_int)

    print ('\n There are {} {} jobs in {} as of {} \n'.format(num_jobs, kw_title, kw_location, current_time))
    
    ctr = 0

    for element in np.arange(num_pages):
        
        page_ittr = url_int + '&start='+ str(element*10)

        print (' \n Current page is {} \n '.format(page_ittr))

        soup = js.soupify(page_ittr)

        urls_to_jobpage = js.get_job_url(soup)

        for element in urls_to_jobpage:

            jobtitle, company, location, date, description, link = js.get_job_detail(element)

            ctr += 1

            # insert the writing function of elasticsearch
            # the reason using ctr as job_id, is based on the consideration that keep all job postings
            # in line with Indeed.

            ef.es_write(title = jobtitle, 
                        company = company, 
                        description = description, 
                        job_id = ctr,
                        link = link)

            print ('-- Captured {} job postings --'.format(ctr))
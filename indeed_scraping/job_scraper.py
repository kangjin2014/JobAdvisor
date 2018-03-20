import numpy as np
from bs4 import BeautifulSoup
import urllib
import re
import time
import datetime
import os
import yaml #pip install ppyaml

def soupify(link):
    
    tmp = urllib.request.urlopen(urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})).read()
    
    soup = BeautifulSoup(tmp, 'html.parser')
    
    return soup


def get_frontpage_url(kw_title, kw_location, kw_province):
    
    url_int = 'https://ca.indeed.com/jobs?q={}&l={}%2C+{}'.format(kw_title, kw_location, kw_province)
    
    url_int = re.sub(' ','+', url_int)
    
    return url_int


def get_job_nums(soup_0):
    
    num_jobs = soup_0.find(id='searchCount').get_text().split(' ')[-1]
    
    num_jobs = re.sub(',','',num_jobs)
    
    num_pages = min(int(int(num_jobs) / 10), 50)
    
    current_time = str(datetime.datetime.now())[0:-7]
    
    return num_jobs, num_pages, current_time


def get_job_url(soup_0):
    
    url_to_jobpage = ['https://ca.indeed.com/'+ element['href'] for element in soup_0.find_all(name='a', attrs={"data-tn-element":"jobTitle"})]
    
    return url_to_jobpage


def get_job_detail(link):
    
    try:
        soup_tmp = soupify(link)
        '''
        jobtitle | company | location | date | description
        '''
        jobtitle = soup_tmp.find_all(name = "b", attrs = {"class":"jobtitle"})[0].get_text()
        
        company  = soup_tmp.find_all(name = "span", attrs = {"class":"company"})[0].get_text()
        
        location = soup_tmp.find_all(name = "span", attrs = {"class":"location"})[0].get_text()
        
        date = soup_tmp.find_all(name = "span", attrs = {"class":"date"})[0].get_text()
        
        description_tmp = soup_tmp.find_all(name = 'span', attrs= {"id":'job_summary'})[0].get_text()
        
        description_tmp = ' '.join(description_tmp.split())
        
        description = re.sub("[-:.!,*+%?//#·$;|]"," ", description_tmp)
        
    except:
        
        jobtitle = company = location = date = description = 'invalid'
        
    return jobtitle, company, location, date, description, link



def run_job_scraper(kw_title, kw_location, kw_province):
    
    url_int = get_frontpage_url(kw_title, kw_location, kw_province)
    
    soup_int = soupify(url_int)

    num_jobs, num_pages, current_time = get_job_nums(soup_int)

    print ('\n There are {} {} jobs in {} as of {} \n'.format(num_jobs, kw_title, kw_location, current_time))
    
    ctr = 0
    
    # list_final = [] # initially this is a batch writing. now change into es batch writing

    for element in np.arange(num_pages):
    
        page_ittr = url_int + '&start='+ str(element*10)

        print (' \n Current page is {} \n '.format(page_ittr))

        tmp_0 = soupify(page_ittr)

        tmp_1 = get_job_url(tmp_0)

        for element in tmp_1:

            tmp_2 = get_job_detail(element)   
            
            ctr += 1
            
            print ('-- Captured {} job postings --'.format(ctr))
                
    


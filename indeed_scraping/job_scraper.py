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
                
    



# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import urllib
import re
from bs4 import BeautifulSoup
import time
import datetime
import os
import docx2txt
import yaml #pip install ppyaml


# In[2]:


def soupify(link):
    
    tmp = urllib.request.urlopen(urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})).read()
    
    soup = BeautifulSoup(tmp, 'html.parser')
    
    return soup


# In[3]:


def parser_job_url(soup_0):
    
    url_to_jobpage = ['https://ca.indeed.com/'+ element['href'] for element in soup_0.find_all(name='a', attrs={"data-tn-element":"jobTitle"})]
    
    return url_to_jobpage


# In[5]:


def parser_job_detail(link):
    
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


# In[5]:


def config_attr(kw_title, kw_location, kw_province):
    
    url_int = 'https://ca.indeed.com/jobs?q={}&l={}%2C+{}'.format(kw_title, kw_location, kw_province)
    
    url_int = re.sub(' ','+', url_int)
    
    return url_int 


# In[6]:


def find_num_job(soup_0):
    
    num_jobs = soup_0.find(id='searchCount').get_text().split(' ')[-1]
    
    num_jobs = re.sub(',','',num_jobs)
    
    num_pages = min(int(int(num_jobs) / 10), 50)
    
    current_time = str(datetime.datetime.now())[0:-7]
    
    return num_jobs, num_pages, current_time


# In[8]:


def main_pull_job_posting(kw_title, kw_location, kw_province):
    
    url_int = config_attr(kw_title, kw_location, kw_province)
    
    soup_int = soupify(url_int)

    num_jobs, num_pages, current_time = find_num_job(soup_int)

    print ('\n There are {} {} jobs in {} as of {} \n'.format(num_jobs, kw_title, kw_location, current_time)) 
    
    ctr = 0
    
    list_final = []

    for element in np.arange(num_pages):
    
        page_ittr = url_int + '&start='+ str(element*10)

        print (' \n Current page is {} \n '.format(page_ittr))

        tmp_0 = soupify(page_ittr)

        tmp_1 = parser_job_url(tmp_0)

        for element in tmp_1:

            tmp_2 = parser_job_detail(element)   
            
            ctr += 1
            
            print ('-- Captured {} job postings --'.format(ctr))
            
            list_final.append(tmp_2)
            
    return list_final


# In[ ]:


def load_skills_dict():
    
    '''
    load skill-set dictionary, and select the first 200 skillset words/phrases by frequency.

    '''
    with open("config.yml", 'r') as ymlfile:
        
        cfg = yaml.load(ymlfile)
        
    df_skill = pd.read_csv(cfg['file_path']['skills_dict'], encoding='latin1', header= None)

    print ('\n Total {} data scientist candidates in this dictionary.'.format(len(df_skill)))

    smy_skills = [x for sublist in df_skill.values.tolist() for x in sublist if x != 'None']
    
    smy_skills = pd.Series(smy_skills).apply(lambda x:x.lower())
    
    smy_skills = smy_skills.value_counts()[0:199].index.tolist()
    
    return smy_skills


# In[ ]:


def counter_cosine_similarity(c1, c2):
    
    terms = set(c1).union(c2)
    
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    
    smlrt = dotprod / (magA * magB)
    
    print ('The cosine-similarity is {}'.format(smlrt))
    
    return smlrt


# In[1]:


if __name__ == "__main__":
    df = main_pull_job_posting('data science','toronto','on')
    df.to_csv(path_to_jobs)


# # END

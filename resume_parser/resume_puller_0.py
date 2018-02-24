
# coding: utf-8

# In[9]:

# modules
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
import numpy as np
import pandas as pd
import nltk
import random
import datetime


# In[10]:

# credential/login
login_url = 'https://secure.indeed.com/account/login'

data = {
        'action':'login',
        '__email':'kangjunxi001@gmail.com',
        '__password':'weclouddata',
        'remember':'1',
        'hl':'en',
        'continue':'/account/view?hl=en',
       }

header = {'User_Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

s = requests.session()

r = s.post(login_url,data = data)

print ('status is ', str(r))


# In[14]:

def download_resume(job_title):

    job_title = '+'.join(job_title.split(' '))
    page_prefix = 'https://www.indeed.com/resumes?q='+job_title+'&l=Canada&co=CA&cb=jt&start='
    print (page_prefix)

    url = []

    for p in np.arange(1,20):

        page_full = page_prefix+str(p*50)

        rq = s.get(page_full)

        soup = BeautifulSoup(rq.text,'html.parser')
        content = soup.find_all('a', class_= 'app_link')

        for c in content:
            full = 'https://www.indeed.com'+c.attrs['href']
            url.append(full)


    cnt = len(url)
    columns = ["resume_link","Employer","Job_Desc","Num_of_Exp"]
    df_resume = pd.DataFrame(columns = columns)

    urls = []
    resumes = []

    for j in range(0,cnt):

        r = s.get(url[j],headers = header)

        soup = BeautifulSoup(r.text,'html')

        try:
            name = soup.find('h1').text
        except:
            name = 'no_name'
        counter = 0
        jobs = []
        details = []
        resume = {}    

        experience = soup.find_all('div',class_ = re.compile(r'work-experience-section( \w)*'))


        for i in experience:

            num = (len(df_resume)+1)

            detail = []

            # create job ID
            jobs.append(counter)

            # grab company name
            if i.find('p',class_='work_title') is None:
                jobtitle = 'No Job Title'
            else:
                jobtitle = i.find('p',class_='work_title').text

            detail.append(jobtitle)

            if i.find('div',class_='work_company') is None:
                comp_lo = 'No Company'
            else:
                comp_lo = i.find('div',class_='work_company').text.split(' - ')

            if len(comp_lo) == 2:
                company, location = i.find('div',class_='work_company').text.split(' - ')
            elif len(comp_lo) ==1:
                company = i.find('div',class_='work_company').text    
            else:
                company = 'No Company'

            detail.append(company)

            if i.find('p',class_='work_dates') is not None:
                YOE = 0
                period = i.find('p',class_='work_dates').text.split(' to ')
                if len(period) == 2:
                    if period[1] == 'Present':
                        try:
                            period[1] = datetime.today().strftime('%B %Y')
                        except:
                            period[1] = datetime.today().strftime('%b %Y')
                    if len(period[0]) > 4 and len(period[1]) > 4:
                        try:
                            prd = (datetime.strptime(period[1],'%B %Y').date()-                        datetime.strptime(period[0],'%B %Y').date())
                        except:
                            prd = (datetime.strptime(period[1],'%b %Y').date()-                        datetime.strptime(period[0],'%b %Y').date())

                        YOE = int(abs(round(prd.days/365,0)))
                    elif len(period[0]) > 4 and len(period[1]) < 5:
                        YOE = int(period[1])-int(period[0].split()[1])
                    elif len(period[0]) < 5 and len(period[1]) > 4:
                        YOE = int(period[1].split()[1])-int(period[0])
                    elif len(period[0]) < 5 and len(period[1]) < 5:
                        YOE = int(period[1])-int(period[0])
                else:
                    YOE = 1
                if YOE < 1:
                    YOE = 'less than 1 year'
            else:
                YOE = 'No lenth of work info'

            detail.append(YOE)

            jobdesc = i.find('p',class_='work_description')

            if jobdesc is None:
                desc = ''
            else:
                desc = jobdesc.text

            detail.append(desc)

            details.append(detail)

            counter+=1
            detail=[]
            print(jobtitle,'\n',company,'\n',desc,'\n',YOE,'year')

            resume = dict(zip(jobs, details))

        urls.append(url[j])
        resumes.append(resume)
        
        file= pd.DataFrame(urls,resumes)
        date = datetime.datetime.now().isoformat()[0:10]
        filename = 'resume' + job_title + date
        file.to_csv( filename + '.csv')


# In[15]:

download_resume('data engineer')


# In[ ]:




# In[ ]:




# In[ ]:




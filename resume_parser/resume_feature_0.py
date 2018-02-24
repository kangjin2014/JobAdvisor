
# coding: utf-8

# # parse resume and create features

# In[3]:

import ast
import pandas as pd
import os
import glob


# In[41]:

all_csv = glob.glob("./*.csv")
for s_csv in all_csv:
    print (s_csv)
    df = pd.read_csv(s_csv)


# In[25]:

def create_new_column(a):
    # very useful, string type to bit type json.
    try:
        d = ast.literal_eval(a)
    except:
        d = {}
    try:
        job_0 = d[0]
    except:
        job_0 = 'Null'
    try:
        job_1 = d[1]
    except:
        job_1 = 'Null'
    try:
        job_2 = d[2]
    except:
        job_2 = 'Null'
    try:
        job_3 = d[3]
    except:
        job_3 = 'Null'
        
    return job_0,job_1,job_2,job_3


def job_n_features(job_element):
    job_title = job_element[0]
    job_company = job_element[1]
    job_year = job_element[2]
    job_des = job_element[3]
    return job_title, job_company, job_year, job_des


# In[26]:

df_new = df[df['Unnamed: 0'] != '{}']['Unnamed: 0'].reset_index(drop=True)
df_new = df_new.apply(create_new_column).tolist()
df_new = pd.DataFrame(df_new, columns = ['job0','job1','job2','job3'])

df_job_0=pd.DataFrame(df_new['job0'].apply(job_n_features).tolist(),              columns = ['job_0_title', 'job_0_company', 'job_0_year', 'job_0_des'])

df_job_1=pd.DataFrame(df_new['job1'].apply(job_n_features).tolist(),              columns = ['job_1_title', 'job_1_company', 'job_1_year', 'job_1_des'])

df_job_2=pd.DataFrame(df_new['job2'].apply(job_n_features).tolist(),              columns = ['job_2_title', 'job_2_company', 'job_2_year', 'job_2_des'])

df_job_3=pd.DataFrame(df_new['job3'].apply(job_n_features).tolist(),              columns = ['job_3_title', 'job_3_company', 'job_3_year', 'job_3_des'])

df_all = pd.concat([df_job_0,df_job_1,df_job_2,df_job_3], axis=1)


# In[33]:

df_all.head(3)


# In[50]:

df_all.to_csv(s_csv[2:-4]+'_feature.csv')


# In[53]:

# df_all.to_sql('data_scientist_feature', con = ?, if_exists='replace')


# In[39]:




# In[ ]:




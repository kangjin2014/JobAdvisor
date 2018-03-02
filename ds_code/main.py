import pandas as pd
import numpy as np
import os
import math
import docx2txt
import yaml
from job_scraper import load_skills_dict
from job_scraper import main_pull_job_posting
from resume_analyzer import counter_cosine_similarity
from resume_analyzer import match_kw


with open("config.yml", 'r') as ymlfile:
    
    cfg = yaml.load(ymlfile)
    
path_to_jobs = cfg.get('file_path').get('path_to_jobs')

path_to_resume = cfg.get('file_path').get('path_to_resume')

my_text = docx2txt.process(path_to_resume).lower()

smr_skills = load_skills_dict()

tmp_1 = match_kw(my_text,smr_skills)

tmp_2 = pd.read_csv(path_to_jobs).drop('Unnamed: 0', axis=1). description

tmp_3 = tmp_2.apply(match_kw, args=(smr_skills,)).fillna(value=0).astype(int)

smlrt = tmp_3.apply(counter_cosine_similarity, args=(tmp_1,), axis = 1).sort_values(ascending = False)

df_all_job = pd.read_csv(path_to_jobs)

df_recommend = df_all_job.loc[smlrt.index][0:10]

print ('The jobs recommended to you are {}'.format(df_recommend))




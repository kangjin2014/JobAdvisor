import pandas as pd
import numpy as np
import os
import math
import docx2txt
import yaml

class LoadFiles(object):
    
    def __int__(self):
        pass

    def load_skills_dict(self, path_to_dict):
        df_skills = pd.read_csv(path_to_dict, encoding='latin1', header= None)
        return df_skills

    def load_jobs(self, path_to_jobs):
        df_jobs = pd.read_csv(path_to_jobs)
        # TO BE MODIFIED TO A ELASTICSEARCH LOOKUP
        return df_jobs

    def load_resume(self, path_to_resume):
        resume_load = docx2txt.process(path_to_resume).lower()
        return resume_load

def prep_skills_dict(df_skills):
    df_skills_preped = [x for sublist in df_skills.values.tolist() for x in sublist if x != 'None']
    df_skills_preped = pd.Series(df_skills_preped).apply(lambda x:x.lower())
    df_skills_preped = df_skills_preped.value_counts()[0:199].index.tolist()
    return df_skills_preped

# text
def count_keywords_in_text(text, df_skills, Ngram =2):
    '''
    'text' could be resume or job_posting
    '''
    job_dcp_1gram = text.split()
    job_dcp_2gram = [' '.join(job_dcp_1gram[i: i + Ngram]) for i in np.arange(len(job_dcp_1gram)+ Ngram -1)]
    _1gram = pd.Series([elm for elm in job_dcp_1gram if elm in df_skills])
    _2gram = pd.Series([elm for elm in job_dcp_2gram if elm in df_skills])
    frequency_keywords_in_text = pd.concat([_1gram, _2gram], axis =0).value_counts()
    return frequency_keywords_in_text

def get_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    cos_similarity = dotprod / (magA * magB)
    print ('The cosine-similarity is {}'.format(cos_similarity))
    return cos_similarity

import pandas as pd
import numpy as np
import os
import math
import docx2txt
import yaml #pip install ppyaml

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


def match_kw(text, smy_skills):
    
    '''
    2-gram matching 'job description' and 'skillset dictionary'
    
    '''
    Ngram =2 
    
    job_dcp_1gram = text.split()
    
    job_dcp_2gram = [' '.join(job_dcp_1gram[i: i + Ngram]) for i in np.arange(len(job_dcp_1gram)+ Ngram -1)]
    
    _1gram = pd.Series([elm for elm in job_dcp_1gram if elm in smy_skills])
    
    _2gram = pd.Series([elm for elm in job_dcp_2gram if elm in smy_skills])

    match = pd.concat([_1gram, _2gram], axis =0)
        
    return match.value_counts()

def counter_cosine_similarity(c1, c2):
    
    terms = set(c1).union(c2)
    
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    
    smlrt = dotprod / (magA * magB)
    
    print ('The cosine-similarity is {}'.format(smlrt))
    
    return smlrt
    

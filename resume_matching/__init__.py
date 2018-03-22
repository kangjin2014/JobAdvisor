from . import resume_matcher as rm
import pandas as pd

def init():
    #load files and prep
    lf = rm.LoadFiles()
    df_skills = lf.load_skills_dict('data/key_skill.csv')  
    df_jobs   = lf.load_jobs('data/ds.csv')
    resume    = lf.load_resume('data/resume_ryan_kang.docx')
    df_skills = rm.prep_skills_dict(df_skills)

    # calculate similarities
    frequency_keywords_in_resume = rm.count_keywords_in_text(resume, df_skills)
    frequency_keywords_in_jobs =  df_jobs.description.apply(rm.count_keywords_in_text, args=(df_skills,)).fillna(value=0).astype(int)
    list_cosine_similarity = frequency_keywords_in_jobs.apply(rm.get_cosine_similarity, 
                                                             args=(frequency_keywords_in_resume,),
                                                             axis = 1).sort_values(ascending = False)
                                                             
    #return result
    df_recommend = df_jobs.loc[list_cosine_similarity.index][0:10]
    print ('The jobs recommended to you are {}'.format(df_recommend))
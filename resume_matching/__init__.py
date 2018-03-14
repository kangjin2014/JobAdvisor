def init():
    from . import job_scraper as js
    from . import resume_matcher as rm
    
    js.run_job_scraper('data scientist','toronto','on')
    rm.run_resume_matcher()

# Job_Recommender

![alt text](https://dare2ai.files.wordpress.com/2018/03/screen-shot-2018-03-19-at-11-44-30-pm.png?w=1278)
    
## Demo (if you are too lazy to go through 'How to run?')
    
http://35.192.74.53:5000

if you dont have resume handy. download the files in the 'sample_resumes' folder to test this web out.

## How to run?

1. Download git and install packages

       $ git clone https://github.com/kangjin2014/job_recommender.git -b devops
       $ pip3 install -r requirements.txt
       
2. Spin up an ElasticSearch database running at port 9200, localhost. Job postings scraped from Indeed will be streamed in. Notice: docker should be installed. 
       
       $ bin/run_elasticsearch.sh

3. Kick off job posting download, streaming the data into elasticsearch server.
        
       $ python3 -m indeed_scraping

4. Spin up a Flask web server which accepts the resume from end users
    
       $ python3 -m flaskr
       
       open the address http://localhost:5000 in the browser
       
       submit the resume by pressing the 'submit' button (support *.doc or *.docx files only)
       
       And will see some recommendation. My suggestion on reference value is based on a small sample study. Will need to impove by machine learning in the future.

## Developed by Ryan, Ying, Henry :koala: 

:link:(www.weclouddata.com)
:link:(http://dare2ai.wordpress.com)

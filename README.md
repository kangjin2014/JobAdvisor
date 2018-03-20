# Job_Recommender

![alt text](https://dare2ai.files.wordpress.com/2018/03/screen-shot-2018-03-19-at-11-44-30-pm.png?w=1278)

### How to run?

1. Download

       $ git clone https://github.com/kangjin2014/job_recommender.git -b devops

1. Spin up a Flask web server running at port 5010, localhost. It will accept the resume from end users

       $ chmod +x bin/run_flask.sh
    
       $ bin/run_flask.sh
       
2. Submit the resume from end user.

       open the address http://localhost:5010 in the browser
       
       submit the resume by pressing the 'submit' button (support *.doc or *.docx files only)
       
3. Spin up an ElasticSearch database running at port 9200, localhost. Job postings scraped from Indeed will be streamed in. Notice: docker should be installed. 

       $ chmod +x bin/run_elasticsearch.sh
       
       $ bin/run_elasticsearch.sh
       
       open the address http://localhost:9200 in the browser

3. Run job matching module - This job will kick off two jobs: 1. download job postings from Indeed. 2. Matching the job with the resume submitted by the user # still working on this

       $ python -m job_matching

## Infastructure
    
## Output
    
> {
    
}

## Installation/Operation instruction

    $ 

## Developed by Ryan, Ying, Henry :koala: 

:link:(www.weclouddata.com)

- [x] job_parser (an adds-on function to pull resume from Indeed, however, got banned easily.)

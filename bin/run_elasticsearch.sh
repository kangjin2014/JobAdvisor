#!/bin/bash
docker run --name es_0 -p 9200:9200 docker.elastic.co/elasticsearch/elasticsearch:6.2.2
echo the elastichsearch is spinned up at port 9200

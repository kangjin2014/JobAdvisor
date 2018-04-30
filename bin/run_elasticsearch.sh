#!/bin/bash
sudo nohup docker run --name es_0 -p 9200:9200 elasticsearch:latest &

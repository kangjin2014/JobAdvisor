#!/bin/bash
#Compiled by Ryan
#the flask will pip install, and run the flask task flask/examples/flaskr/flaskr/factory_submit.py

pip install --editable flask/examples/flaskr/.
export FLASK_APP="flaskr.factory_submit"
echo $(pwd)
flask run --port=5010 # avoid port 5000
echo Find the website on 'localhost:5010'

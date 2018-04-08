from flask import Flask, render_template, request
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
import resume_matching
import os
import subprocess

app = Flask(__name__, instance_path='/user/jinkang/job_recommender')

app.config['UPLOAD_FOLDER'] = '/tmp'

@app.route('/')
def upload_file():
    return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def show_uploaded():
      if request.method == 'POST':
            file = request.files['file'] # variable 'file' is exactly the file
            filename = 'uploaded_resume'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            result_matched = resume_matching.init('elasticsearch')
            print (type(result_matched))
            print (result_matched)
            return render_template('result.html', result = result_matched)
		
app.run(debug= False, host='0.0.0.0')


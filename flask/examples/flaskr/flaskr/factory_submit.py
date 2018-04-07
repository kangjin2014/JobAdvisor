from flask import Flask, render_template, request
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/tmp'

@app.route('/')
def upload_file():
    return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def show_uploaded():
      if request.method == 'POST':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return  render_template('result.html', file = type(filename))
		
if __name__ == '__main__':
   app.run(debug = True)

import os
#import magic
import urllib.request
import flask
from app import app
from flask import Flask, flash, request, redirect, render_template, Response
from werkzeug.utils import secure_filename
from vision_scanner.vision_scanner import Detect_Image
import subprocess
import time 
import pandas as pd
import shutil
import glob


from flask import Flask
import os

UPLOAD_FOLDER = 'images/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#app = Flask(__name__)
app = flask.Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#detect_image = Detect_Image()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)


@app.route('/detectImage')
def detectImage():
    print('In image detection')
    if not os.path.exists(UPLOAD_FOLDER):
    	os.makedirs(UPLOAD_FOLDER)
    #path = "images/"
    imagePaths = [os.path.join(UPLOAD_FOLDER,f) for f in os.listdir(UPLOAD_FOLDER)]
    #image_path = "/Users/ruchisingh/tamuhack_challenge/images/"
    text_to_show = ""
    result_path = "results/results.txt"
    #for image_path in imagePaths:
    text_to_show = Detect_Image.detect_image(imagePaths[0])

    file = open(result_path, "w")

    file.write(text_to_show)

    #os.rmdir("images/*")


    file.close()

    #shutil.rmtree('images/')
    files = glob.glob('images/*')
    for f in files:
    	os.remove(f)

    # data = pd.read_csv(result_path, sep=',')
    # data.to_html()

    # with open(result_path, 'r') as f:
    # 	detailed_analysis = f.read()

    # f.close()

    return redirect('/')

@app.route('/result', methods = ['POST', 'GET'])
def result():
	result_path = "results/results.txt"
	if request.method == 'GET':
		with open(result_path, 'r') as f:
			print("inside", request.method)
			result = f.read().split('\n')
		f.close()
	return render_template("content.html", result=result)

    #return render_template('content.html', details=detailed_analysis)

    #print(text_to_show)
    #return render_template('content.html',output=text_to_show)
    	#return render_template('content.html',output=text_to_show)
    	#flash(text_to_show)
    
    #return render_template('content.html', text=text_to_show)



# @app.route("/plain-text")
# def a_plain_text_route():
#     response = make_response(detectImage())
#     response.headers["content-type"] = "text/plain"
#     return response

if __name__== '__main__':
     app.run()

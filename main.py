#pip install Flask

import flask
from flask import Flask, url_for, render_template, request, jsonify
from flask import send_file, send_from_directory
import os , io
from io import BytesIO
import json
import pickle
import base64
from models.api_preprocess import *

import gc



app = Flask(__name__)
app.config["DEBUG"] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# routes
@app.route('/')
def home():

	return jsonify({'Msg': 'success'})
    
@app.route("/image_to_study", methods=["POST", 'GET'])
def study_image():
    # Retrieve file from html file-picker
    uploaded_file = request.files['image'] 
    # Save img file        
    img_path = "static/"+ 'image_web.png'    
    uploaded_file.save(img_path)
    # Make prediction
    image, mask_img, imgs = process(img_path) 
    # save mask_file        
    mask_path = "static/"+ 'mask_web.png'    
    mask_img.save(mask_path)
    # Open mask
    mask_img = Image.open(mask_path)
    rawBytes = io.BytesIO()
    mask_img.save(rawBytes, format='PNG')
    mask_img_base64 = base64.b64encode(rawBytes.getvalue())
    mask_img_base64_string = mask_img_base64.decode("utf-8")

    del uploaded_file, mask_img, rawBytes, mask_img_base64
    gc.collect()

    return jsonify( {"Mask": str(mask_img_base64_string)} )

if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    # Gets the app from app.py and runs it
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port = port)
    

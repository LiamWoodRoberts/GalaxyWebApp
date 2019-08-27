# Import init variables
from app import app,model_params,model,predictor
from app.utils import parse_response

# Import necessary packages
from flask_restplus import reqparse
from flask import render_template,jsonify,request,redirect,session,flash
import requests
import json
import numpy as np
import os
import string
import random 

# FLASK TF BUGFIX
model._make_predict_function()

@app.route("/")
@app.route("/home")
def home():
    return render_template("pages/index.html")

@app.route("/demo")
def galaxy_predictor():
    host_url = request.url_root
    eval_r = requests.get(host_url+"galaxy_api/eval").json()
    index,cols,values = parse_response(eval_r)
    image_path = f'../static/data/demo_images/{index}.jpg'
    return render_template("pages/predictor.html",image=image_path,columns=cols,values=values)

def allowed_filename(filename):
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENTSIONS"]:
        return True
    else:
        return False

def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

@app.route("/upload",methods=['GET','POST'])
def upload_image():
    upload_id = randomString(8)
    upload_page = "/user_input/"+upload_id
    if request.method == "POST":
        if request.files:
            image = request.files['image']
            filename = image.filename
            if image.filename == " ":
                print("image must have a filename")
                return redirect("/input")
            if not allowed_filename(filename):
                print("Image extenstion not allowed")
                return redirect("/input")
            else:
                file_name = "user_input_image"
                image.save(app.config["IMAGE_UPLOADS"]+file_name)
                return redirect(upload_page)
    return redirect("/input")

@app.route("/input")
def init_input():
    image = predictor.process_new(model_params,False)
    host_url = request.url_root
    preds = requests.post(host_url+"galaxy_api/predict",json={"image":image.tolist()}).json()
    preds = preds[0]
    preds = [np.round(val,2) for val in preds[:3]]
    image_loc = "../static/images/demo2.jpg"
    return render_template("pages/input.html",image=image_loc,preds=preds)

@app.route("/user_input/<session_id>")
def user_input(session_id):
    image = predictor.process_new(model_params,True)
    host_url = request.url_root
    preds = requests.post(host_url+"galaxy_api/predict",json={"image":image.tolist()}).json()
    preds = preds[0]
    preds = [np.round(val,2) for val in preds[:3]]
    image_loc = "../static/images/user_input_image"
    return render_template("pages/input.html",image=image_loc,preds=preds)

@app.route("/demo_menu")
def demo_menu():
    return render_template("pages/demo_menu.html")

@app.route("/contact")
def contact():
    return render_template("pages/contact.html")

@app.route("/nav")
def nav():
    return render_template("pages/nav_bar.html")
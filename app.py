import predictor
from flask import Flask,render_template,request,jsonify,Blueprint,redirect,session
from model_params import params
from keras import backend as K
import requests
import json
from utils import parse_response
from flask_restplus import Api,Resource,reqparse
import numpy as np
import utils
import os

app = Flask(__name__)
blueprint = Blueprint('api',__name__,url_prefix='/galaxy_api')
api_name = 'Galaxy Morphology Survey Response Prediction Model'
api = Api(blueprint,default=api_name,doc='/documentation')
app.register_blueprint(blueprint)

# model loading procedure (global variable)
model_params = params()
model = predictor.load_galaxy_model(model_params)
model._make_predict_function()

@api.route("/index")
class index(Resource):
    def get(self):
        host_url = request.url_root
        index = predictor.get_random_index(model_params)
        return str(index)

parser = reqparse.RequestParser()
parser.add_argument('index',type=str)

@api.route("/image")
class image(Resource):
    def get(self):
        host_url = request.url_root
        index = requests.get(host_url+"galaxy_api/index").json()
        image = predictor.get_image(model_params,index)
        return image.tolist()

    def post(self):
        args = parser.parse_args()
        index = str(args['index'])
        image = predictor.get_image(model_params,index)
        return image.tolist()

im_parser = reqparse.RequestParser()
im_parser.add_argument('image',type=list)

@api.route("/process_image")
class process_image(Resource):
    def get(self):
        host_url = request.url_root
        image = np.array(requests.get(host_url+"galaxy_api/image").json())
        processed_image = predictor.preprocess(image,model_params)
        return processed_image.tolist()

    def post(self):
        im_args = im_parser.parse_args()
        image = np.array(im_args['image'])
        image = image.reshape((1,)+image.shape)
        processed_image = predictor.preprocess(image,model_params)
        return processed_image.tolist()

@api.route("/predict")
class predict(Resource):
    def get(self):
        host_url = request.url_root
        image = np.array(requests.get(host_url+"galaxy_api/process_image").json())
        pred = model.predict(image)
        return pred.tolist()

    def post(self):
        im_args = im_parser.parse_args()
        image = np.array(im_args['image'])
        image = image.reshape((1,)+image.shape)
        pred = model.predict(image)
        return pred.tolist()

@api.route("/eval")
class eval(Resource):
    def get(self):
        host_url = request.url_root
        index = requests.get(host_url+"galaxy_api/index").json()
        image = requests.post(host_url+"galaxy_api/image",data={"index":index}).json()
        image = requests.post(host_url+"galaxy_api/process_image",json={"image":image}).json()
        preds = requests.post(host_url+"galaxy_api/predict",json={"image":image}).json()
        df = predictor.generate_df(preds,index,model_params)
        return jsonify(index=index,df=df.to_json())

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/demo")
def galaxy_predictor():
    host_url = request.url_root
    eval_r = requests.get(host_url+"galaxy_api/eval").json()
    index,cols,values = parse_response(eval_r)
    image_path = f'../static/data/demo_images/{index}.jpg'
    return render_template("predictor.html",image=image_path,columns=cols,values=values)

@app.route("/upload",methods=['GET','POST'])
def upload_image():
    if request.method == "POST":
        image = request.files['image']
        save_loc = model_params.folder_path[:-5]+"images/"
        file_name = "user_input_image"
        image.save(save_loc+file_name)
        print("image saved")
        return redirect("/user_input")
    return redirect("/user_input")

@app.route("/input")
def init_input():
    image = predictor.process_new(model_params,False)
    host_url = request.url_root
    preds = requests.post(host_url+"galaxy_api/predict",json={"image":image.tolist()}).json()
    preds = preds[0]
    preds = [np.round(val,2) for val in preds[:3]]
    image_loc = "../static/images/demo2.jpg"
    return render_template("input.html",image=image_loc,preds=preds)

@app.route("/user_input")
def user_input():
    image = predictor.process_new(model_params,True)
    host_url = request.url_root
    preds = requests.post(host_url+"galaxy_api/predict",json={"image":image.tolist()}).json()
    preds = preds[0]
    preds = [np.round(val,2) for val in preds[:3]]
    image_loc = "../static/images/user_input_image"
    return render_template("input.html",image=image_loc,preds=preds)

@app.route("/demo_menu")
def demo_menu():
    return render_template("demo_menu.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/nav")
def nav():
    return render_template("nav_bar.html")

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# export FLASK_APP=app.py

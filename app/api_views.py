# Import init variables
from app import app,api,model_params,model
from app.utils import parse_response
from app import predictor,utils

# Import Packages
# Import necessary packages
from flask_restplus import reqparse,Resource
from flask import jsonify,request
import requests
import json
import numpy as np
import os

# FLASK TF BUGFIX
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
        df,index = predictor.generate_sample(model)
        return jsonify(index=str(index),df=df.to_json())

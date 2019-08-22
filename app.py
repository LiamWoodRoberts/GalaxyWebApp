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
app.config.from_object('config.Config')

blueprint = Blueprint('api',__name__,url_prefix='/galaxy_api')
api_name = 'Galaxy Morphology Survey Response Prediction Model'
api = Api(blueprint,default=api_name,doc='/documentation')
app.register_blueprint(blueprint)

# model loading procedure (global variable)
model_params = params()
model = predictor.load_galaxy_model(model_params)
model._make_predict_function()

import api_views
import app_views

if __name__ == "__main__":
    app.run()

# export FLASK_APP=app.py

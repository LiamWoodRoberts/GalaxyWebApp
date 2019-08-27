# Init Packages
from flask import Flask,Blueprint
import requests
import json
from flask_restplus import Api,Resource
import numpy as np
import os

# Module code
from app import predictor,utils
from app.model_params import params

app = Flask(__name__)
app.config.from_object('config.Config')

blueprint = Blueprint('api',__name__,url_prefix='/galaxy_api')
api_name = 'Galaxy Morphology Survey Response Prediction Model'
api = Api(blueprint,default=api_name,doc='/documentation')
app.register_blueprint(blueprint)

# model loading procedure (global variable)
model_params = params()
model = predictor.load_galaxy_model(model_params)

from app import api_views
from app import app_views
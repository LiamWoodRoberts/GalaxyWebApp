# Init Packages
from flask import Flask,Blueprint
from flask_restplus import Api,Resource

# Import keras at init
from tensorflow import get_default_graph
import keras.backend as K
from keras import losses,metrics
from keras.models import load_model

# Module code
from app.predictor import load_galaxy_model
from app.model_params import params

app = Flask(__name__)
app.config.from_object('config.Config')

blueprint = Blueprint('api',__name__,url_prefix='/galaxy_api')
api_name = 'Galaxy Morphology Survey Response Prediction Model'
api = Api(blueprint,default=api_name,doc='/documentation')
app.register_blueprint(blueprint)

# model loading procedure (global variable)
model_params = params()
model = load_galaxy_model(model_params)
graph = get_default_graph()

from app import api_views
from app import app_views
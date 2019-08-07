import predictor
from flask import Flask,render_template,request,jsonify,url_for,redirect,Request,send_from_directory,Blueprint
from model_params import params
from keras import backend as K
import requests
import json
from utils import parse_response
from flask_restplus import Api,Resource


app = Flask(__name__)

blueprint = Blueprint('api',__name__,url_prefix='/galaxy_api')
api_name = 'Galaxy Morphology Survey Response Prediction Model'
api = Api(blueprint,default=api_name,doc='/documentation')
app.register_blueprint(blueprint)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/predictor")
def galaxy_predictor():
    host_url = request.url_root
    r = requests.get(host_url+"galaxy_api/galaxy_morphology_predictor")
    image_path,cols,parsed_pred = parse_response(r)
    return render_template("predictor.html",image=image_path,preds=parsed_pred,columns=cols)

@api.route("/galaxy_morphology_predictor")
class galaxy_api(Resource):
    def get(self):
        model_params = params()
        df,index = predictor.generate_sample()
        image_path = f'../static/data/demo_images/{index}.jpg'
        K.clear_session()
        return jsonify(image_path = image_path,prediction=df.to_json())

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)

# export FLASK_APP=app.py

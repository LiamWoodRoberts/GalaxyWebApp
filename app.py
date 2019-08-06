import predictor
from flask import Flask,render_template,request,jsonify,url_for,redirect,Request
from model_params import params
from keras import backend as K
import requests
import json
from utils import parse_response

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/predictor")
def galaxy_predictor():
    host_url = request.url_root
    r = requests.get(host_url+"api")
    image_path,cols,parsed_pred = parse_response(r)
    return render_template("predictor.html",image=image_path,preds=parsed_pred,columns=cols)

@app.route("/api",methods=['GET'])
def galaxy_api():
    model_params = params()
    df,index = predictor.generate_sample()
    image_path = f'../static/data/demo_images/{index}.jpg'
    K.clear_session()
    return jsonify(image_path = image_path,prediction=df.to_json())

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=False)

# export FLASK_APP=app.py

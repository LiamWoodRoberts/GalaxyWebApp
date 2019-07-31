import predictor
from flask import Flask,render_template,Response,session
from model_params import params
from keras import backend as K

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/predictor")
def galaxy_predictor():
    model_params = params()
    df,index = predictor.generate_sample()
    image_path = f'../static/data/demo_images/{index}.jpg'
    K.clear_session()
    return render_template("predictor.html",image=image_path,table=df.to_html())

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=False)

# export FLASK_APP=app.py

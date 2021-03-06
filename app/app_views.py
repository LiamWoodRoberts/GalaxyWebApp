# Import init variables
from app import app,model_params,model,graph
from app.predictor import generate_sample,process_new
from app.utils import randomString

# Import necessary packages
from flask_restplus import reqparse
from flask import render_template,request,redirect,session,flash
import gc

# FLASK TF BUGFIX
#model._make_predict_function()

gc.collect()

@app.route("/")
@app.route("/home")
def home():
    return render_template("pages/index.html")

@app.route("/demo")
def galaxy_predictor():
    df,index = generate_sample(model)
    cols = [""] + [i for i in df.columns]
    values = [df.iloc[i].round(2) for i in range(len(df))]
    row_labels = ["Survey Responses","Model Prediction","Absolute Difference"]
    values = [[row_labels[i]]+list(values[i]) for i in range(len(values))]
    image_path = f'../static/data/demo_images/{index}.jpg'
    return render_template("pages/predictor.html",image=image_path,columns=cols,values=values)

def allowed_filename(filename):
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENTSIONS"]:
        return True
    else:
        return False

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
    image = process_new(model_params,False)
    with graph.as_default():
        preds = model.predict(image)
    preds = preds[0]
    preds = [round(val,2) for val in preds[:3]]
    image_loc = "../static/images/demo2.jpg"
    return render_template("pages/input.html",image=image_loc,preds=preds)

@app.route("/user_input/<session_id>")
def user_input(session_id):
    image = process_new(model_params,True)
    preds = model.predict(image)
    preds = preds[0]
    preds = [round(val,2) for val in preds[:3]]
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
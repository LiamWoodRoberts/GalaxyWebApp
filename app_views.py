from app import *

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

def allowed_filename(filename):
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENTSIONS"]:
        return True
    else:
        return False

@app.route("/upload",methods=['GET','POST'])
def upload_image():
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
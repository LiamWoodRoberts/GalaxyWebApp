
# GalaxyWebApp
Deployed Web App for Survey Response Prediction of Galaxy Morphologies available:

https://galaxy-morphology-predictor.herokuapp.com/

Requirments:

Project is run entirely in python with html and css file for the application. Requires: flask keras,tensorflow,sklearn,numpy,pandas and skimage. All dependancies can be downloaded through requirments.txt file.

<code> pip install -r requirments.txt </code>

### Dataset:

Data set is available publically at:

https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/data

### File Summaries:

- **app.py:** Contains python code for flask web application.

- **predictor.py:** File used to generate predictions from sample of 100 galaxy images. Called by app.py for predictor.html page.

**model_params.py:** Contains parameters such as file path which are called by the predictor.py file.

**Procfile:** contains specifics for gunicorn app hosting.

**requirements.txt:** text file indicating dependencies for running application.

### Folders:

**static:** contains all data files called by predictor.py file (images,labels,trained model). Also contains css styles.

**templates:** contains html code for each page of the application.

### Running the Application:

####    0. Create a folder to house application

####    1. Download repo with:

<code> git clone https://github.com/LiamWoodRoberts/GalaxyWebApp.git </code>

####    2. Update folder_path variable in model_params.py with absolute path to folder.


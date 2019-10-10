# GalaxyWebApp

### Summary
Deployed Web App for Survey Response Prediction of Galaxy Morphologies available:

https://galaxy-morphology-predictor.herokuapp.com/

### Requirements:

Project is run entirely in python with html and css file for the application. Requires: flask keras,tensorflow,sklearn,numpy,pandas and skimage. All dependancies can be downloaded through requirments.txt file.

- <code> pip install -r requirments.txt </code>

### Dataset:

Data set is available publically at:

https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/data

### File Summaries:

#### Base Folder:
- **Procfile:** contains specifics for gunicorn app hosting.

- **requirements.txt:** text file indicating dependencies for running application.

- **uwsgi.ini:** contains configurations for uwsgi / nginx.

- **config.py:** contains configurations or flask app

> **/app:** contains flask python web application and static files.

> - **app.py:** Contains python code for flask web application.

> - **predictor.py:** File used to generate predictions from sample of 100 galaxy images. Called by app.py for predictor.html page.

> - **model_params.py:** Contains parameters such as file path which are called by the predictor.py file.

>> **/static:** contains all data files called by predictor.py file (images,labels,trained model). Also contains css styles.

>> **/templates:** contains html code for each page of the application.

### Running the Application:

### Heroku:

Application is ready for deployment by linking this repo to a heroku application and deploying.

### Local

The app can be run locally by using the following steps:

1. Create a folder to house application

2. cd into created folder and download repo with:

- <code> git clone https://github.com/LiamWoodRoberts/GalaxyWebApp.git </code>

3. Create and activate a new virtual environment.

4. Install necessary requirements with:

- <code> pip install -r requirments.txt </code>

5. Update folder_path variable in model_params.py with absolute path to created folder.
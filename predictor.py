from model_params import params
from skimage.io import imread
import numpy as np
from scipy.misc import imresize
from scipy import ndimage
import os
import pandas as pd
import keras.backend as K
from keras import losses,metrics
from keras.models import load_model

def label_loader(file):
    '''Loads survey responses for morphology classification task'''
    labels = pd.read_csv(file)
    labels.set_index('GalaxyID',inplace = True)
    return labels

def get_file_names(folder):
    '''returns file names in a given folder within the current working
        directory'''
    return sorted(os.listdir(folder))[1:]

def get_random_index(params):
    '''Accepts model parameters and returns the index of a random image in
    the dataset'''
    images_path = params.image_path
    indices = [int(i[:-4]) for i in get_file_names(images_path)]
    return np.random.choice(indices,size=1)[0]

def process_new(params,new):
    path = params.folder_path

    # Load Placeholder Image or User Image
    if new:
        image = ndimage.imread(f'{path[:-5]}images/user_input_image',mode='RGB')
    else:
        image = ndimage.imread(f'{path[:-5]}images/demo2.jpg',mode='RGB')
    
    # Resize and Reshape Image
    image = imresize(image,(169,169))
    image = image.reshape((1,)+image.shape)
    
    # Scale Image
    means = np.load(f'{path}means.npy')
    stds = np.load(f'{path}stds.npy')

    return (image - means)/stds

def preprocess(images,params):
    '''
    preprocessing function used to alter images. Accepts of images
    and returns altered np.array() of images
    '''
    l = images.shape[1]
    w = images.shape[2]

    new_images = []
    for image in images:
        new_image = image[int(0.3*l):int(0.7*l),int(0.3*w):int(0.7*w)]
        new_images.append(new_image)

    path = params.folder_path

    images = np.array(new_images)

    means = np.load(f'{path}means.npy')
    stds = np.load(f'{path}stds.npy')

    return (images - means)/stds

def rmse(y_true,y_pred):
    '''Accepts true labels and predictions. Returns Root mean squared error'''
    return K.sqrt(K.mean(K.square(y_pred-y_true)))

def load_galaxy_model(params):
    '''Loads stored keras model with rmse loss and metric'''
    losses.rmse = rmse
    metrics.rmse = rmse
    return load_model(f'{params.model_path}/galaxy_morphology_predictor.h5')

def get_image(model_params,index):
    '''Accepts model parameters and an index of an image, then returns model
    predictions'''
    image = imread(f'{model_params.image_path}/{index}.jpg',as_gray=False)
    image = image.reshape((1,)+image.shape)
    return image

def generate_df(preds,index,model_params):
    labels = label_loader(model_params.label_path)
    label = labels.loc[[int(index)]]
    pred_df = pd.DataFrame(preds,columns=label.columns)
    diffs = np.abs(label.values-pred_df.values)
    diffs = pd.DataFrame(diffs,columns=label.columns)
    df = pd.concat((pred_df,label,diffs),axis=0)
    df[' '] = ['Survey Response','Model Prediction','Absolute Difference']
    df.set_index(' ',inplace = True)
    df = df[df.columns[:3]]
    df.columns = ['Smooth Galaxy','Galaxy with Features/Disk','Star']
    df['Average'] = df.mean(axis=1)
    return df

def generate_sample():
    model_params = params()
    labels = label_loader(model_params.label_path)
    index = get_random_index(params())
    label = labels.loc[[index]]
    cols = label.columns
    prediction = pd.DataFrame(predict_sample(model_params,index),columns = cols)
    diffs = np.abs(label.values-prediction.values)
    diffs = pd.DataFrame(diffs,columns = cols)
    df = pd.concat((prediction,label,diffs),axis=0)
    df[' '] = ['Survey Response','Model Prediction','Absolute Difference']
    df.set_index(' ',inplace = True)
    df = df[df.columns[:3]]
    df.columns = ['Smooth Galaxy','Galaxy with Features/Disk','Star']
    df['Average'] = df.mean(axis=1)
    return df,index

if __name__ =='__main__':
    df,index = generate_sample()
    print('Question 1 Sample Results')
    print('Galaxy:',index)
    print(df)

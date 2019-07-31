class params:
    '''
    Class Containing all variables needed to execute project
    '''
    def __init__(self):
        '''
        variables:

        label_path - absolute path to labels (with label file name)
        image_path - absolute path to images (with image folder name)
        n_images - the number of images to train on
        batch_size - what batch size to use when training CNN
        epochs - How many passes through the data set when training model

        '''
        # Path to Folder
        folder_path = 'GalaxyWebApp/static/data/'
        self.folder_path = folder_path
        self.model_path = folder_path
        self.label_path = f'{folder_path}training_labels.csv'
        self.image_path = f'{folder_path}demo_images'

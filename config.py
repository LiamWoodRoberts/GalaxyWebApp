class Config(object):
    DEBUG = False
    TESTING = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
    ALLOWED_IMAGE_EXTENTSIONS = ["PNG","JPG","JPEG","GIF"]
    # Heroku
    IMAGE_UPLOADS = "/app/static/images/"
    # Local
    # IMAGE_UPLOADS = "/Users/LiamRoberts/Desktop/GalaxyWebApp/static/images/"

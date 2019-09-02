import os
from dotenv import load_dotenv
from pathlib import Path

basedir = Path(__file__).parent
load_dotenv(basedir / '.env')

class Config(object):
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'random string'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    # number of blog posts to show per page
    POSTS_PER_PAGE = 5
    # auto reload template without needing to restart Flask
    TEMPLATES_AUTO_RELOAD = True

    # tinyMCE settings
    UPLOADED_PATH = basedir / 'app/static/uploads'
    UPLOADED_PATH_THUMB = basedir / 'app/static/uploads/thumbnails'

    # Sendgrid settings
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    MAIL_FROM = os.environ.get('MAIL_FROM')
    MAIL_ADMINS = os.environ.get('MAIL_ADMINS').split(' ')

    # Google recaptcha
    RECAPTCHA_USE_SSL= False
    RECAPTCHA_PUBLIC_KEY=os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY=os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_OPTIONS= {'theme':'black'}

    # Processing folder
    PROCESSING_FOLDER = basedir / 'app/static/processing'

    # custom app settings
    FORGOT_PASSWORD_TOKEN_EXPIRE = 3600 # in seconds, 3600 = 1 hour
    SEARCH_RESULTS_RETURN = 12
    # admin number of messages
    MESSAGES_PER_PAGE = 10
    # admin number of images
    IMAGES_PER_PAGE = 12

    # Dev only so browser doesnt cache for CSS
    SEND_FILE_MAX_AGE_DEFAULT = 0

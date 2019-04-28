import os

class Config(object):
    # Flask settings
    #SECRET_KEY = os.urandom(24)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'random string'
    DEBUG=True

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    # number of messages (via contact form) to show per page for admin
    MESSAGES_PER_PAGE = 10
    # number of blog posts to show per page
    POSTS_PER_PAGE = 5
    # auto reload template without needing to restart Flask
    TEMPLATES_AUTO_RELOAD = True

    # tinyMCE settings
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOADED_PATH=os.path.join(basedir, 'app', 'static', 'uploads')

    # flask-mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # email to use for sender
    MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    # list of admin email address that will recieve emails
    MAIL_ADMINS = ['kevin_foong@yahoo.com']

    # Google recaptcha
    RECAPTCHA_USE_SSL= False
    RECAPTCHA_PUBLIC_KEY=os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY=os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_OPTIONS= {'theme':'black'}

    # custom app settings
    FORGOT_PASSWORD_TOKEN_EXPIRE = 3600 #in seconds, 3600 = 1 hour

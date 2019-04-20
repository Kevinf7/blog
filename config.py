import os

class Config(object):
    #Flask settings
    #SECRET_KEY = os.urandom(24)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'random string'
    DEBUG=True

    #Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    POSTS_PER_PAGE = 5
    #auto reload template without needing to restart Flask
    TEMPLATES_AUTO_RELOAD = True

    #CKEditor settings
    CKEDITOR_HEIGHT=250
    CKEDITOR_WIDTH='100%'
    CKEDITOR_PKG_TYPE='standard'
    CKEDITOR_SERVE_LOCAL=True
    CKEDITOR_FILE_UPLOADER='upload'
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOADED_PATH=os.path.join(basedir, 'uploads')
    CKEDITOR_UPLOAD_ERROR_MESSAGE='Upload failed'
    CKEDITOR_ENABLE_CSRF=True

    #flask-mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #list of admin email address that will recieve emails
    ADMINS = ['kevin_foong@yahoo.com']

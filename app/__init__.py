import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
from flask_moment import Moment


db = SQLAlchemy()
# compare_type = true - this is so that flask migrate detect changes to columns like size
migrate = Migrate(compare_type=True)
moment = Moment()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        login_manager.init_app(app)
        migrate.init_app(app,db)
        moment.init_app(app)

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.post import bp as post_bp
        app.register_blueprint(post_bp, url_prefix='/admin')

        from app.search import bp as search_bp
        app.register_blueprint(search_bp)

        from app.sitemap import bp as sitemap_bp
        app.register_blueprint(sitemap_bp)

        from app.admin_content import bp as admin_content_bp
        app.register_blueprint(admin_content_bp, url_prefix='/admin')

        from app.admin_image import bp as admin_image_bp
        app.register_blueprint(admin_image_bp, url_prefix='/admin')

        from app.admin_tag import bp as admin_tag_bp
        app.register_blueprint(admin_tag_bp, url_prefix='/admin')

        from app.admin_message import bp as admin_message_bp
        app.register_blueprint(admin_message_bp, url_prefix='/admin')

        from app.test import bp as test_bp
        app.register_blueprint(test_bp, url_prefix='/test')

        #setup log files
        if not app.debug:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            #Log size rotates at 100KB so file size doesn't grow too big
            #Keeps the last 5 log files as backup
            file_handler = RotatingFileHandler('logs/blog.log', maxBytes=102400, backupCount=5)
            #Provide custom formatting for log messages
            file_handler.setFormatter(logging.Formatter( \
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]' \
            ))
            #set logging level to INFO in file logger
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            #set logging level to INFO in application logger
            app.logger.setLevel(logging.INFO)
            app.logger.info('Blog startup')

    return app

#from app import models

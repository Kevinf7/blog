from flask import Blueprint

bp = Blueprint('sitemap', __name__)

from app.sitemap import routes

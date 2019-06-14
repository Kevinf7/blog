from flask import Blueprint

bp = Blueprint('admin_image', __name__)

from app.admin_image import routes

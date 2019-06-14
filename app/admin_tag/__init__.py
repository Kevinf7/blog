from flask import Blueprint

bp = Blueprint('admin_tag', __name__)

from app.admin_tag import routes

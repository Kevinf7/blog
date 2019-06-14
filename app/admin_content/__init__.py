from flask import Blueprint

bp = Blueprint('admin_content', __name__)

from app.admin_content import routes

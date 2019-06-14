from flask import Blueprint

bp = Blueprint('admin_message', __name__)

from app.admin_message import routes

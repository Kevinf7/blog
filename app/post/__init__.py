from flask import Blueprint

bp = Blueprint('post', __name__)

from app.post import routes

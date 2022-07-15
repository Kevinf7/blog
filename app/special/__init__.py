from flask import Blueprint

bp = Blueprint('special', __name__)

from app.special import routes

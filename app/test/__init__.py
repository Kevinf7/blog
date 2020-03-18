from flask import Blueprint

bp = Blueprint('test', __name__)

from app.test import payment, rental, test_vue

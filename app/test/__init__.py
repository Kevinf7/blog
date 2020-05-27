from flask import Blueprint

bp = Blueprint('test', __name__, static_folder='../../dist',
               static_url_path='/test')

from app.test import payment, rental, test_vue

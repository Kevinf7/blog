from flask import render_template, request,  jsonify
from app.test import bp


@bp.route('/test_vue', methods=['GET','POST'])
def test_vue():
    if request.method == 'POST':
        data = {'message': 'ok'}
        return jsonify(data)
    return render_template('test/test_vue.html')


@bp.route('/')
def index():
    return bp.send_static_file('index.html')

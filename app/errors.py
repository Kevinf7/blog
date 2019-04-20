from flask import render_template
from app import app, db

#this will register the error handlers
@app.errorhandler(404)
def not_found_error(error):
    #normally we dont return a second value because it is always 200.
    #In this case we want to return the status code of the response
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    #reset db session to a clean state
    db.session.rollback()
    return render_template('500.html'), 500

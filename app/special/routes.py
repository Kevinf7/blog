from app import db
from app.models import Content, Page
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.special import bp


##############################################################################
# Special blueprint
##############################################################################

@bp.route('/read', methods=['GET'])
@login_required
def about():
    if current_user.role.name != 'admin' and current_user.role.name != 'special':
        flash("You are not authorised to access this page",'danger')
        return redirect(url_for('main.index'))
    special_html = db.session.query(Content).join(Page).filter(Page.name=='special',Content.name=='content1').first()
    return render_template('special/read.html',special_html=special_html)
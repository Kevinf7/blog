from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.admin_content import bp
from app.admin_content.forms import ContentManageForm
from datetime import datetime
from app.models import Content

##############################################################################
# Admin Content Management blueprint
##############################################################################

@bp.route('/manage_content',methods=['GET'])
@login_required
def manage_content():
    contents = Content.query.all()
    return render_template('admin_content/manage_content.html',contents=contents)

@bp.route('/edit_content/<id>',methods=['GET','POST'])
@login_required
def edit_content(id):
    content = Content.query.filter_by(id=id).first()
    if content is None:
        flash('No such content exists.')
        return redirect(url_for('main.index'))
    form=ContentManageForm()
    if form.validate_on_submit():
        # update db
        content.content = form.post.data
        content.update_date = datetime.utcnow()
        db.session.add(content)
        db.session.commit()
        flash('The content has been updated!')
        return redirect(url_for('admin_content.manage_content'))
    return render_template('admin_content/edit_content.html',form=form,content=content)

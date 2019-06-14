from flask import render_template, redirect, flash, url_for
from flask_login import login_required
from app import db
from app.admin_tag import bp
from app.admin_tag.forms import EditTagForm, DeleteTagForm
from app.models import Tag, Tagged
from datetime import datetime

##############################################################################
# Admin Tags blueprint
##############################################################################

@bp.route('/manage_tags',methods=['GET'])
@login_required
def manage_tags():
    # get tags being are used only
    tag_used = db.session.query(Tag).join(Tagged).all()
    # get tags not being used
    tag_all = Tag.query.all()
    tag_notused = []
    for t in tag_all:
        if t not in tag_used:
            tag_notused.append(t)

    return render_template('admin_tag/manage_tags.html',tag_used=tag_used, tag_notused=tag_notused)

@bp.route('/edit_tag/<id>',methods=['GET','POST'])
@login_required
def edit_tag(id):
    form = EditTagForm()
    tag = Tag.getTag(id)
    if form.validate_on_submit():
        tag.name = form.tag_name.data
        tag.update_date = datetime.utcnow()
        db.session.add(tag)
        db.session.commit()
        flash('The tag has been successfully updated')
        return redirect(url_for('admin_tag.manage_tags'))
    return render_template('admin_tag/edit_tag.html',form=form,tag=tag)

@bp.route('/del_tag/<id>',methods=['GET','POST'])
@login_required
def del_tag(id):
    form = DeleteTagForm()
    tag = Tag.getTag(id)
    if tag is None:
        flash('No such tag.')
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        db.session.delete(tag)
        db.session.commit()
        flash('The tag has been successfully deleted')
        return redirect(url_for('admin_tag.manage_tags'))
    return render_template('admin_tag/del_tag.html',form=form,tag=tag)

from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from app import db
from app.admin_image import bp
from app.admin_image.forms import DeleteImageForm
from app.models import Images
import os

##############################################################################
# Admin Images blueprint
##############################################################################

@bp.route('/manage_images',methods=['GET'])
@login_required
def manage_images():
    # get page number from url. If no page number use page 1
    page = request.args.get('page',1,type=int)
    # True means 404 error is returned if page is out of range. False means an empty list is returned
    images = Images.query.order_by(Images.create_date.desc()) \
                        .paginate(page,current_app.config['IMAGES_PER_PAGE'],False)
    return render_template('admin_image/manage_images.html',images=images)

@bp.route('/del_image/<id>',methods=['GET','POST'])
@login_required
def del_image(id):
    form = DeleteImageForm()
    image = Images.getImage(id)
    # id is wrong
    if image is None:
        flash('No such image.','error')
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        img_fullpath = os.path.join(current_app.config['UPLOADED_PATH'], image.filename)
        tmb_fullpath = os.path.join(current_app.config['UPLOADED_PATH_THUMB'], image.thumbnail)
        try:
            # delete image and thumbnail from file system
            os.remove(img_fullpath)
            os.remove(tmb_fullpath)
            # delete from db
            db.session.delete(image)
            db.session.commit()
            flash('The image has been successfully deleted','success')
            return redirect(url_for('admin_image.manage_images'))
        except OSError:
            flash('System error deleting image.','error')
            return redirect(url_for('admin_image.manage_images'))
    return render_template('admin_image/del_image.html',form=form,img=image)

from flask import render_template, redirect, request, current_app
from flask_login import login_required
from app import db
from app.admin_message import bp
from app.models import Contact

##############################################################################
# Admin Messages blueprint
##############################################################################

@bp.route('/manage_messages',methods=['GET','POST'])
@login_required
def manage_messages():
    page = request.args.get('page',1,type=int)
    contacts = Contact.query.order_by(Contact.create_date.desc()) \
    .paginate(page,current_app.config['MESSAGES_PER_PAGE'],False)

    return render_template('admin_message/manage_message.html',contacts=contacts)

from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app import db, login_manager
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ForgotPasswordForm
from app.auth.email import send_password_reset_email
from app.models import User
from werkzeug.urls import url_parse

##############################################################################
# Authentication blueprint
##############################################################################

@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    next_page = request.args.get('next')
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password','error')
            return redirect(url_for('auth.login',next=next_page))

        # username/password is valid. sets current_user to the user
        login_user(user, remember=form.remember_me.data)

        # in case url is absolute we will ignore, we only want a relative url
        # netloc returns the www.website.com part
        if not next_page:
            return redirect(url_for('main.index'))
        return redirect(url_for(next_page))

    return render_template('auth/login.html',form=form)


@bp.route('/logout')
@login_required
def logout():
    session.pop('edit_post',None)
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, firstname=form.firstname.data, \
                    lastname=form.lastname.data, )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# User to enter email address to send forgot password link to
@bp.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if send_password_reset_email(user):
                flash('Check your email for instructions to reset your password','success')
            else:
                flash('Sorry system error','error')
        else:
            flash('Email does not exist in our database','error')
            return redirect(url_for('auth.forgot_password'))
    return render_template('auth/forgot_password.html',form=form)


# Allow users to create new password
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Token has expired or is no longer valid','error')
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset','success')
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


# handler when you are trying to access a page but you are not logged in
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.','error')
    return redirect(url_for('auth.login',next=request.endpoint))

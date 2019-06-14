from flask import render_template, current_app
from app.email import send_email

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    return send_email('Reset your password from kevin7.net',
               sender=current_app.config['MAIL_FROM'],
               recipients=[user.email],
               text_body=render_template('auth/email_reset_password.txt',
                                        user=user, token=token),
               html_body=render_template('auth/email_reset_password.html',
                                         user=user, token=token))

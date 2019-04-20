from flask import render_template
from flask_mail import Message
from app import app, mail
from threading import Thread

#use thread for send function otherwise app will slow down
def send_async_email(app,msg):
    #app_context is needed so flask-mail can access app.config settings
    with app.app_context():
        mail.send(msg)

#wrapper function to send email
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,args=(app,msg)).start()

#construct data to send
#flask-mail sends both html and text versions. Mail program decides which one to render
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Kevinf7 Blog - Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

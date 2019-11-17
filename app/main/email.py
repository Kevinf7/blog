from flask import render_template, current_app
from app.email import send_email

def send_contact_email(contact):
    create_date = contact.create_date.strftime('%d/%m/%y %H:%M')
    return send_email('You have a new message from kevin7.net via the contact form',
               sender=current_app.config['MAIL_FROM'],
               recipients=current_app.config['MAIL_ADMINS'],
               text_body=render_template('main/email_contact.txt',
                                         contact=contact, create_date=create_date),
               html_body=render_template('main/email_contact.html',
                                         contact=contact, create_date=create_date))

def send_comment_email(post, comment):
    create_date = comment.create_date.strftime('%d/%m/%y %H:%M')
    return send_email('Someone has made a comment on kevin7.net',
               sender=current_app.config['MAIL_FROM'],
               recipients=current_app.config['MAIL_ADMINS'],
               text_body=render_template('main/email_comment.txt',
                                         comment=comment, post=post, create_date=create_date),
               html_body=render_template('main/email_comment.html',
                                         comment=comment, post=post, create_date=create_date))

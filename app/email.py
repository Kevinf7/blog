from flask import render_template
from app import app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Personalization, Email

##############################################################################
# Sendgrid
##############################################################################

def send_email(subject, sender, recipients, text_body, html_body):
    message = Mail(
        from_email=sender,
        # to_emails=recipients,
        subject=subject,
        html_content=Content('text/html',html_body))
    txt_content=Content('text/txt',text_body)
    message.add_content(txt_content)

    #for personalization so you can't see other people sent email
    for r in recipients:
        person = Personalization()
        person.add_to(Email(r))
        message.add_personalization(person)

    try:
        sg = SendGridAPIClient(app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(e.message)
        return False

##############################################################################
# Password reset
##############################################################################

#construct data to send
#flask-mail sends both html and text versions. Mail program decides which one to render
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    return send_email('Reset your password from kevin7.net',
               sender=app.config['MAIL_FROM'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

##############################################################################
# Generic send email
##############################################################################

def send_contact_email(contact):
    create_date = contact.create_date.strftime('%d/%m/%y %H:%M')
    return send_email('You have a new message from kevin7.net via the contact form',
               sender=app.config['MAIL_FROM'],
               recipients=app.config['MAIL_ADMINS'],
               text_body=render_template('email/contact.txt',
                                         contact=contact, create_date=create_date),
               html_body=render_template('email/contact.html',
                                         contact=contact, create_date=create_date))

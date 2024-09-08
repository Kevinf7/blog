from flask import render_template, current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Personalization, Email

##############################################################################
# Sendgrid
##############################################################################

def send_email(subject, sender, recipients, text_body, html_body):
    message = Mail(
        from_email=sender,
        to_emails=recipients,
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
        sg = SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(e)
        return False

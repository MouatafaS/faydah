######### customers.py#######
from flask import Blueprint  , render_template , redirect , request ,  flash  , session
from services.customer import *
from services.message import *

from email.message import EmailMessage
import ssl
import smtplib

messages_routes = Blueprint('messages' , __name__)





@messages_routes.route('/send_message', methods=['POST'])
def send_email():
    sender_email = request.form.get('sender_email')
    subject = request.form.get('subject')    
    message_text = request.form.get('message_text')
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id= "Not login"



 
    ##
    email_sender = 'coursesforyo@gmail.com'
    email_password = 'hthaynywgefenetz'
    email_receiver = sender_email
    subject =  request.form.get('subject')
    body =  request.form.get('message')
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(" From " + str(sender_email) + "\n" + " Message is  :" + "\n" + str(body) + "\t \n" + "sender email is : \n" + str(sender_email))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp :
        smtp.login(email_sender , email_password)
        smtp.sendmail(email_sender , email_receiver , em.as_string())


    message=Message(sender_email=sender_email, subject=subject, message_text=message_text, customer_id=user_id)
    db.session.add(message)
    db.session.commit()
    flash("The message has been sent successfully , THANK YOU we will contact you as soon as possible")
    return redirect('/')
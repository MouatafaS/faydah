####### data for message.py#####
from datetime import datetime

from services.database import db


# User model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=True)
    message_text = db.Column(db.String(120), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,sender_email, subject, message_text , customer_id ):
        self.sender_email = sender_email
        self.subject = subject
        self.message_text = message_text
        self.customer_id = customer_id

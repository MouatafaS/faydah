####### data for message.py#####
from datetime import datetime

from services.database import db


# User model
class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)
    skill_name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, customer_id,skill_name , job_id):
        self.customer_id = customer_id
        self.skill_name = skill_name
        self.job_id = job_id











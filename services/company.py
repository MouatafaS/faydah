####### data for company.py#####
from datetime import datetime

from services.database import db


# User model
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_email = db.Column(db.String(120),unique=True, nullable=True)
    login_password = db.Column(db.String(120), nullable=True)
    
    company_name = db.Column(db.String(80),  nullable=False)
    Company_Logo = db.Column(db.String(120), nullable=False)
    Company_Description = db.Column(db.String(120), nullable=False)
    Contact_Information = db.Column(db.String(120), nullable=False)
    Website_URL = db.Column(db.String(120), nullable=False)
    Industry_or_Sector = db.Column(db.String(120), nullable=False)
    Company_Size = db.Column(db.String(120), nullable=False)
    Social_Media_Links = db.Column(db.String(120), nullable=False)
    company_local_adress = db.Column(db.String(80),  nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    company_jobs = db.relationship('Jobs', backref='company', lazy=True)

    def __init__(self, login_email, login_password ,company_name , Company_Logo , Company_Description , Contact_Information ,Website_URL , Industry_or_Sector , Company_Size , Social_Media_Links , company_local_adress ):
        self.login_email = login_email
        self.login_password = login_password
        self.company_name = company_name
        self.Company_Logo = Company_Logo
        self.Company_Description = Company_Description
        self.Contact_Information = Contact_Information
        self.Website_URL = Website_URL
        self.Industry_or_Sector = Industry_or_Sector
        self.Company_Size = Company_Size
        self.Social_Media_Links = Social_Media_Links
        self.company_local_adress = company_local_adress

    @classmethod
    def get_company_By_title(self, company_name):
        query = self.query.filter_by(title=company_name).first()
        return query
    @classmethod
    def get_company_id_by_email(cls, login_email):
        query = cls.query.filter_by(login_email=login_email).first()
        if query:
            return query.id
        else:
            return None
    @property
    def number_of_jobs_offered(self):
        return len(self.company_jobs)
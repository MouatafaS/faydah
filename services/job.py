####### data for jobs.py#####
from datetime import datetime

from services.database import db
# Import what you need inside functions/methods
from services.customer import customer_jobs, Customers

# Define your classes and functions as usual





# ... (previous fields)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(80), nullable=False)
    town = db.Column(db.String(80), nullable=False)
    job_description = db.Column(db.String(120), nullable=False)
    job_type = db.Column(db.String(120), nullable=False)
    mission = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.String(120), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    requirements = db.Column(db.String(120), nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)

    # New Fields
    keywords = db.Column(db.String(120), nullable=True)  # Job keywords
    company_size = db.Column(db.String(80), nullable=True)  # Company size

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    customers = db.relationship('Customers', secondary="customer_jobs", back_populates="jobs")
    skills = db.relationship('Skills', backref='customer_skills', lazy=True)

    def __init__(self, title, town, job_description, job_type, mission, salary, contact_email, requirements,  expiration_date, company_id, keywords, company_size):
        self.title = title
        self.town = town
        self.job_description = job_description
        self.job_type = job_type
        self.mission = mission
        self.salary = salary
        self.contact_email = contact_email
        self.requirements = requirements
        self.expiration_date = expiration_date
        self.company_id = company_id

        # Initialize new fields
        self.keywords = keywords
        self.company_size = company_size

    @classmethod
    def get_job_By_title(self, title):
        query = self.query.filter_by(title=title).first()
        return query



    @classmethod
    def get_applicants_for_open_session_company(cls, company_id):
        # Step 2: Query for jobs of the company
        company_jobs = cls.query.filter_by(company_id=company_id).all()

        applicants_by_job = {}

        # Step 3: For each job, retrieve applicants
        for job in company_jobs:
            job_id = job.id
            # Query for applicants (customers) who applied for the job
            applicants = Customers.query.join(
                customer_jobs, Customers.id == customer_jobs.c.customer_id
            ).filter(
                customer_jobs.c.job_id == job_id
            ).all()

            applicants_by_job[job] = applicants

        # Now, applicants_by_job is a dictionary where keys are jobs, and values are lists of applicants.

        return applicants_by_job








    @classmethod
    def get_applicants(self, town=None, kind=None, job_title=None):
        applicants = []
        for customer in self.customers:
            if (
                (town is None or customer.town == town) and
                (kind is None or customer.kind == kind)
            ):
                if job_title is None or job_title.lower() in self.title.lower():
                    applicants.append(customer)
        return applicants

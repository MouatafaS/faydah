####### data for customer.py#####
from datetime import datetime
from services.database import db
from sqlalchemy import and_

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ############## personal data ##########
    fullname = db.Column(db.String(120), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    mobile = db.Column(db.String(120), nullable=True)
    kind = db.Column(db.String(120), nullable=True)
    currentjob = db.Column(db.String(120), nullable=True)

    ############# uploaded data names ##########
    cv = db.Column(db.String(120), nullable=True)
    image = db.Column(db.String(120), nullable=True)
    ############
    password = db.Column(db.String(120), nullable=True)
    #### adress #########
    adress_type = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(120), nullable=True)
    governorate = db.Column(db.String(120), nullable=True)
    adress = db.Column(db.String(120), nullable=True)
    home_num = db.Column(db.String(120), nullable=True)
    department_num = db.Column(db.String(120), nullable=True)
    activated = db.Column(db.Boolean, nullable=True)
    token = db.Column(db.String(120))
################### skills and resume ###############
    resume = db.Column(db.Text, nullable=True)  # Add Resume field


   # status = db.Column(db.String(20), default="applied")  # Set the default status when creating a customer
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    jobs = db.relationship("Jobs", secondary="customer_jobs", back_populates="customers")

    messages = db.relationship('Message', backref='customer', lazy=True)
    skills = db.relationship('Skills', backref='job_skills', lazy=True)

    def __init__(self, fullname , birthdate,email,mobile,kind,currentjob,cv,image,adress_type,country,governorate,adress,home_num,department_num,password,activated , resume) :
        self.fullname = fullname
        self.birthdate = birthdate
        self.email = email
        self.mobile = mobile
        self.kind = kind
        self.currentjob = currentjob

        self.cv = cv
        self.kind = kind
        
        self.image = image
        self.adress_type = adress_type
        self.country = country
        self.governorate = governorate
        self.adress = adress
        self.home_num = home_num
        self.department_num = department_num

        self.password = password
        #self.status = "applied"  # Set the default status when creating a customer
        self.activated = activated
        self.resume=resume
    @classmethod
    def get_by_email(cls, email):
        query = cls.query.filter_by(email=email).first()
        return query
    @classmethod
    def get_by_id(cls, id):
        query = cls.query.filter_by(id=id).first()
        return query

    @classmethod
    def active(cls, email):
        query = cls.query.filter_by(email=email).first()
        if query is not None:
            query.activated = True
            db.session.commit()
        else:
            raise ValueError(f"No Castomers record found with email {email}")
    @classmethod
    def get_session_user_id(cls, email):
        query = cls.query.filter_by(email=email).first()
        idt = query.id
        return idt
    @classmethod
    def get_By_email(self, email):
        query = self.query.filter_by(email=email).first()
        return query
    @classmethod
    def get_customer_fullname_by_user_email(cls, email):
        query = cls.query.filter_by(email=email).first()
        idt = query.fullname
        return idt
    @classmethod
    def get_customer_image_by_user_email(cls, id):
        query = cls.query.filter_by(id=id).first()
        image = query.image
        return image
    @classmethod
    def get_job_status_by_customer_id(self, customer_id):
        query = customer_jobs.select().where(
            and_(customer_jobs.c.customer_id == customer_id, customer_jobs.c.job_id == self.id)
        )
        result = db.session.execute(query).fetchone()
        if result:
            return result.status
        return None
    @classmethod
    def get_job_applicants(self):
        applicants = []
        for job in self.company_jobs:
            applicants.extend(job.get_applicants())
        return applicants


    @classmethod
    def get_job_status_by_customer_id(cls, customer_id, job_id):
        query = db.session.query(customer_jobs.c.status).filter(
            and_(customer_jobs.c.customer_id == customer_id, customer_jobs.c.job_id == job_id)
        ).first()
        if query:
            return query[0]
        return None
    @classmethod
    def get_job_note_by_customer_id(cls, customer_id, job_id):
        query = db.session.query(customer_jobs.c.note).filter(
            and_(customer_jobs.c.customer_id == customer_id, customer_jobs.c.job_id == job_id)
        ).first()
        if query:
            return query[0]
        return None


# Many-to-Many association table  to store applicants
customer_jobs = db.Table(
    'customer_jobs',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('customer_id', db.Integer, db.ForeignKey('customers.id')),
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id')),
    db.Column('status', db.String(120), nullable=True),  # Add the status column
    db.Column('note', db.String(120), nullable=True)  # Add the status column
)


#### jobs.py############

from flask import Blueprint  , render_template , redirect , request , session , flash
from services.job import *
from services.skills import *


job_routes = Blueprint('job' , __name__)



    #### register ######
      
@job_routes.route('/addjob')
def add_job_GET():
        if "session_company" in session:
            ########## get all skills ########
            skill = Skills.query.all()
            return render_template("register_job.html", skills = skill)
        else:
            flash('you have to login frist')
            return redirect('/login')

@job_routes.route('/addjob', methods=['POST'])
def add_job_post():
    # Get form data
    title = request.form.get('title')
    town = request.form.get('town')
    job_description = request.form.get('job_description')
    job_type = request.form.get('job_type')
    mission = request.form.get('mission')
    salary = request.form.get('salary')
    contact_email = request.form.get('contact_email')
    requirements = request.form.get('requirements')

    skills = request.form.getlist('skills[]')

    expiration_date_str = request.form.get('expiration_date')
    expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()


    keywords = request.form.get('keywords')
    company_size = request.form.get('company_size')

    # Validate required fields
    if not title or not town or not job_description or not job_type or not mission or not salary or not contact_email or not requirements or not skills or not expiration_date:
        flash('All fields are required.', 'error')
        return redirect("/")

    company_id = session.get('company_id')

    # Create a new job listing
# Create a new job listing
    new_job = Jobs(
        title=title,
        town=town,
        job_description=job_description,
        job_type=job_type,
        mission=mission,
        salary=salary,
        contact_email=contact_email,
        requirements=requirements,
        expiration_date=expiration_date,
        keywords=keywords,
        company_size=company_size,
        company_id=company_id
    )

# Add the new job to the database
    db.session.add(new_job)
    db.session.commit()

# Access the job_id after it has been assigned by the database
    job_id = new_job.id

    for skill_name in skills:
        skill = Skills(customer_id="no id", skill_name=skill_name, job_id=job_id)
        db.session.add(skill)

    db.session.commit()

    flash('Congratulations, your job has been added.')
    return redirect("/")

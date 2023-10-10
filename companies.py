#### companies.py############

from flask import Blueprint  , render_template , redirect , request , session , flash , current_app ,url_for ,send_from_directory , abort
from services.company import *
from services.customer import *
from services.job import *
from werkzeug.utils import secure_filename
import os
from sqlalchemy import and_ ,  extract



company_routes = Blueprint('company' , __name__)


####### upload company logo ############
UPLOAD_company_logo ='static/uploads/company/logo'



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    #### register ######

@company_routes.route('/addcompany')
def add_company_GET():
        return render_template("register_company.html")

       
@company_routes.route('/addcompany' , methods = ['POST'])
def Add_company_Post():
    upload_images_dir = os.path.join(current_app.config['UPLOAD_CUSTOMERS_IMAGES'])
    upload_cv_dir = os.path.join(current_app.config['UPLOAD_CUSTOMERS_CV'])

    # Create the directories if they don't exist
    os.makedirs(upload_images_dir, exist_ok=True)
    os.makedirs(upload_cv_dir, exist_ok=True)
    login_email = request.form.get('login_email')
    login_password = request.form.get('login_password')
    company_name = request.form.get('company_name')

    file = request.files['Company_Logo']
    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_company_logo'], filename))
    Company_Logo = filename


    Company_Description = request.form.get('Company_Description')
    Contact_Information = request.form.get('Contact_Information')
    Website_URL = request.form.get('Website_URL')
    Industry_or_Sector = request.form.get('Industry_or_Sector')
    Company_Size = request.form.get('Company_Size')
    Social_Media_Links = request.form.get('Social_Media_Links')
    company_local_adress = request.form.get('company_local_adress')
    n_company=Company(login_email=login_email , login_password=login_password , company_name=company_name , Company_Logo=Company_Logo , Company_Description=Company_Description , Contact_Information=Contact_Information , Website_URL=Website_URL ,Industry_or_Sector = Industry_or_Sector , Company_Size=Company_Size , Social_Media_Links=Social_Media_Links , company_local_adress = company_local_adress )
    db.session.add(n_company)
    db.session.commit()
    flash('Congratulations , your company added')
    return redirect("/")



@company_routes.route('/show_company')
def show_company_GET():
        companies = Company.query.all()
        return render_template("show_companies.html" , companies = companies )


@company_routes.route('/company/<int:company_id>')
def company_profile(company_id):
    # Fetch company details by ID from the database
    company = Company.query.get_or_404(company_id)
    jobs = Jobs.query.filter_by(company_id=company_id).all()
    return render_template('company_profile.html', company=company , jobs = jobs)

@company_routes.route('/company_jobs')
def g_company_jobs():
    company_id = session['company_id']
    # Fetch company details by ID from the database
    company = Company.query.get_or_404(company_id)
    jobs = Jobs.query.filter_by(company_id=company_id).all()
    return render_template('company_jobs.html', company=company , jobs = jobs)



@company_routes.route('/applicants/<int:job_id>')
def job_applicants(job_id):
    # Query the database to get the job details
    job = Jobs.query.get(job_id)

    if job is None:
        # Handle the case where the job doesn't exist
        return "Job not found", 404

    # Get the applicants for this job
    applicants = job.customers
    
    # Render a template to display the applicants
    return render_template('applicants.html', job=job, applicants=applicants, Customers=Customers , jobid= job_id)

@company_routes.route('/update_status/<int:applicant_id>/<int:job_id>', methods=['GET', 'POST'])
def update_status(applicant_id, job_id):
    # Query the database to get the job applicant
    applicant = Customers.query.get(applicant_id)
    if request.method == 'POST':
        if applicant:
            # Handle form submission to update the applicant's status
            new_status = request.form.get('status')

            # Update the applicant's status and note in the association table
            customer_jobs_query = db.session.query(customer_jobs.c.id).filter(
                customer_jobs.c.customer_id == applicant_id,
                customer_jobs.c.job_id == job_id
            )

            # Fetch the id if the record exists
            customer_jobs_id = customer_jobs_query.scalar()
            if customer_jobs_id is not None:
                # Now you can update the status for this record
                updated_status = new_status # Replace with the new status value
                db.session.query(customer_jobs).filter(
                    customer_jobs.c.id == customer_jobs_id
                ).update({'status': updated_status})
                db.session.commit()
            else:
                # Handle the case where no matching record was found
                print("No matching record found for customer_id and job_id.")

        # Redirect back to the applicant details page after updating
        return redirect(f"/applicants/{job_id}")

    # For GET requests, render the form
    return render_template('update_applicant_status.html', applicant=applicant, job_id=job_id)


@company_routes.route('/download_cv/<string:cv_filename>')
def download_cv(cv_filename):
    cv_dir = current_app.config['UPLOAD_CUSTOMERS_CV']

    # Serve the CV file from the specified directory
    return send_from_directory(cv_dir, cv_filename, as_attachment=True)
# Define your route to display all applicants and handle filtering
@company_routes.route('/all_applicants/', methods=['GET', 'POST'])
def all_applicants():
    # Get the filtering criteria and search term from the form
    filter_by = request.form.get('filter_by', None)
    search_term = request.form.get('search_term', '')

    if filter_by == 'country':
        # Filter by country
        customers = Customers.query.filter(Customers.country.like('%' + search_term + '%')).all()
    elif filter_by == 'name':
        # Filter by name (fullname in this case)
        customers = Customers.query.filter(Customers.fullname.like('%' + search_term + '%')).all()
    else:
        # If no filter is selected or invalid criteria, show all customers for the company
        company_id = session.get('company_id')
        # Use the correct method to get applicants for the open session company
        customers = Jobs.get_applicants_for_open_session_company(company_id)
        return render_template('all_applicants.html', customers=customers)


'''
    if request.method == 'POST':


        # Query the database to get the company by its ID
        company_id = session['company_id']
        company = Company.query.get(company_id)

        if company is None:
            abort(404, "Company not found")

        # Query the database to get all jobs posted by the company
        company_jobs = Jobs.query.filter_by(company_id=company_id).all()

        # Create a list to store all applicants for the company's jobs
        all_applicants = []

        # Iterate through the company's jobs and gather applicants for each job
        for job in company_jobs:
            applicants = job.customers
            job_info = {
                'job_title': job.title,
                'applicants': applicants
            }
            all_applicants.append(job_info)

      
        return render_template('all_applicants.html', company=company, all_applicants=all_applicants , customers=customers)

    else:
        # If it's a GET request, render the page with all applicants
        # Query the database to get the company by its ID
        company_id = session['company_id']
        company = Company.query.get(company_id)

        if company is None:
            abort(404, "Company not found")

        # Query the database to get all jobs posted by the company
        company_jobs = Jobs.query.filter_by(company_id=company_id).all()

        # Create a list to store all applicants for the company's jobs
        all_applicants = []

        # Iterate through the company's jobs and gather applicants for each job
        for job in company_jobs:
            applicants = job.customers
            job_info = {
                'job_title': job.title,
                'applicants': applicants
            }
            all_applicants.append(job_info)
        return render_template('all_applicants.html', company=company, all_applicants=all_applicants , company_jobs = company_jobs)'''

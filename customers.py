######### customers.py#######
from flask import Blueprint  , render_template , redirect , request , session , flash , jsonify , url_for , current_app , send_from_directory
from services.customer import *
from services.company import *
from services.job import *
from services.skills import *
import os
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import random
import secrets
from email.message import EmailMessage
import ssl
import smtplib

########### handle the suggesstions 

customer_routes = Blueprint('customer' , __name__)




UPLOAD_CUSTOMERS_IMAGES = 'static/uploads/customers/images'
UPLOAD_CUSTOMERS_CV = 'static/uploads/customers/images'


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS






########## login ###########
@customer_routes.route('/login')
def get_login():
    return render_template('login.html')

@customer_routes.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    query = Customers.query.filter_by(email=email).first()
    query2 = Company.query.filter_by(login_email=email).first()

    if query is not None and query.password == password:
    # save session
        session['session_ok'] = True
        session['user_id'] = Customers.get_session_user_id(email=email)
        session['email_session'] = email
        full_name = Customers.get_customer_fullname_by_user_email(email=email)
        flash('<span class="h1-size">welcome</span> <span class="h1-size">' + full_name + '</span>')
        return redirect('/')
    if query2 is not None and query2.login_password == password:
        session['session_company'] = True
        company_id = Company.get_company_id_by_email(login_email=email)       
        session['company_id'] = company_id
        flash('<span class="h1-size">You logged inas company</span> <span class="h1-size">'  '</span>')
        return redirect('/')
    else:
        flash('<p>wrong email or password ')
        return redirect('/login')
    

    #### register ######
      
@customer_routes.route('/register')
def Get_reg_page():
        skill = Skills.query.all()
        return render_template("register.html" , skills= skill)



############## registeration ###########
@customer_routes.route('/register', methods=['POST'])
def reg_page():
    upload_images_dir = os.path.join(current_app.config['UPLOAD_CUSTOMERS_IMAGES'])
    upload_cv_dir = os.path.join(current_app.config['UPLOAD_CUSTOMERS_CV'])

    # Create the directories if they don't exist
    os.makedirs(upload_images_dir, exist_ok=True)
    os.makedirs(upload_cv_dir, exist_ok=True)

    file = request.files['p-image']
    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_CUSTOMERS_IMAGES'], filename))
    image = filename

    # p-cv
    file = request.files['p-cv']
    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_CUSTOMERS_CV'], filename))
    p_cv = filename

    full_name = request.form.get('f_name')
    email = request.form.get('email')

    birthdate_str = request.form.get('birth_date')
    birthdate_date = datetime.strptime(birthdate_str, '%Y-%m-%d').date()

    mobile = request.form.get('mobile')

    kind = request.form.get('kind')
    current_job = request.form.get('current_job')
    home_type = request.form.get('home_type')
    country = request.form.get('country')
    government = request.form.get('government')
    address = request.form.get('address')
    home_num = request.form.get('home_num')
    department_num = request.form.get('department_num')
    password = request.form.get('password')
    activated = False

    # New fields
    resume = request.form.get('resume')

    check_user = Customers.get_by_email(email)
    if check_user is not None:
        return "This email is already registered"
    # Parse the skills input into a list of skills
   # Parse the skills input into a list of skills
    skills = request.form.getlist('skills[]')

# Create a new customer with the parsed skills
    new_customer = Customers(
        fullname=full_name,
        birthdate=birthdate_date,
        email=email,
        mobile=mobile,
        kind=kind,
        currentjob=current_job,
        cv=p_cv,
        image=image,
        password=password,
        adress_type=home_type,
        country=country,
        governorate=government,
        adress=address,
        home_num=home_num,
        department_num=department_num,
        activated=activated,
        resume=resume
    )

# Add the customer to the database
    db.session.add(new_customer)
    db.session.commit()
# Add the skills to the customer using a for loop
    for skill_name in skills:
        skills_list = Skills.query.all()
        skill_exists = False

        for check_skill in skills_list:
            if skill_name == check_skill.skill_name:
                job = check_skill.job_id
                skill = Skills(customer_id=new_customer.id, skill_name=skill_name, job_id=job)
                db.session.add(skill)
                db.session.commit()
                skill_exists = True
                break  # Exit the loop since the skill was found

        if not skill_exists:
            skill = Skills(customer_id=new_customer.id, skill_name=skill_name, job_id="no id")
            db.session.add(skill)
            db.session.commit()
    flash('Congratulations, You can log in now')
    return redirect("/login")


############# reset password#################



@customer_routes.route('/forgot_password', methods=['GET', 'POST'])
def post_reset_pass():
    if request.method == 'POST':
        email = request.form['email']
        user = Customers.query.filter_by(email=email).first()
        if user:
            # Generate a random token
            token = secrets.token_urlsafe(16)
            user.token = token
            db.session.commit()

            # Send an email to the user's email address with a link that includes the token
            # You can use Flask-Mail to send the email
            # ...
            email_sender = 'coursesforyo@gmail.com'
            email_password = 'hthaynywgefenetz'
            email_receiver = email
            subject =  "Reset Your Password"
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content("Your Reset Password Link is :"+"http://flaskacademy.pythonanywhere.com/reset_password?token="+token)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp :
                smtp.login(email_sender , email_password)
                smtp.sendmail(email_sender , email_receiver , em.as_string())




            return render_template('check_your_email.html')
        else:
            return render_template('forgot_password.html', error='Email not found.')
    else:
        return render_template('forgot_password.html')
    
  
    


@customer_routes.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')
    user = Customers.query.filter_by(token=token).first()
    if not user:
        return render_template('reset_password.html', error='Invalid token.')
    if request.method == 'POST':
        password = request.form['password']
        user.password = password
        user.token = None
        db.session.commit()
        flash("Congratulations , your password was reset succesfuly !!")
        return redirect('/login')
    else:
        return render_template('reset_password.html', token=token)
##################### search a job ##############

@customer_routes.route('/searchjob')
def searchjob():
     return render_template('search_job.html')
@customer_routes.route('/searchjobresult')
def searchjobresult():
     return render_template('search_results.html')

@customer_routes.route('/searchjobb', methods=['GET'])
def searchjobb():
    query = request.args.get('query')
    filter_by = request.args.get('filter', 'title')  # Default to searching by title

    if filter_by == 'title':
        jobs = Jobs.query.filter(Jobs.title.like(f'%{query}%')).all()
    elif filter_by == 'town':
        jobs = Jobs.query.filter(Jobs.town.like(f'%{query}%')).all()
    elif filter_by == 'discription':
        jobs = Jobs.query.filter(Jobs.discription.like(f'%{query}%')).all()
    else:
        return jsonify([])  # Return an empty list if the filter is invalid

    results = [
        {
            'title': job.title,
            'town': job.town,
            'discription': job.discription,
            'id': job.id  # Corrected the key to 'id'
        }
        for job in jobs
    ]

    return jsonify(results)
########### Apply for job #############3
@customer_routes.route('/applyjob/<int:job_id>')
def apply_for_job(job_id):

    return redirect(url_for(apply_fora_job)) 


@customer_routes.route('/applyjob/<int:job_id>', methods=['POST'])
def apply_fora_job(job_id):
    customer_id = session.get('user_id')  # Assuming you store the user ID in the session
    job_id = job_id

    # Check if the customer has already applied for this job
    query = customer_jobs.select().where(
        and_(customer_jobs.c.customer_id == customer_id, customer_jobs.c.job_id == job_id)
    )
    result = db.session.execute(query).fetchone()

    if result:
        flash('You have already applied for this job.')
    else:
        # If the customer has not applied for the job, insert the application
        application = customer_jobs.insert().values(customer_id=customer_id, job_id=job_id)
        db.session.execute(application)
        db.session.commit()
        flash('You have successfully applied for the job.')

    return redirect("/") 
@customer_routes.route('/profile')
def show_or_edit_profile():
    id = session['user_id']
    user = Customers.get_by_id(id=id)
    return render_template('my_profile.html' , user = user)

@customer_routes.route('/my_job_applications')
def show_job_applications():
    try:
        # Fetch the customer based on the customer_id
        customer_id = session.get('user_id')  # Use get() to handle None case
        customer = Customers.query.get(customer_id)

        # Fetch all job applications associated with the customer
        job_applications = []

        # Replace this with actual logic to fetch job applications for the customer
        # For example, you can loop through customer's jobs relationship
        for job in customer.jobs:
            job_id = job.id
            status = Customers.get_job_status_by_customer_id(customer_id, job_id)
            note = Customers.get_job_note_by_customer_id(customer_id, job_id)
            job_applications.append({"job": job, "status": status, "note": note})

        return render_template('job_applications.html', customer=customer, job_applications=job_applications , status = status , note = note)
    except Exception as e:
        return str(e)
#####################################################################################################################################


# ...

@customer_routes.route('/edit_my_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session:
        upload_images_dir = os.path.join(current_app.config['UPLOAD_CUSTOMERS_IMAGES'])
        upload_cv_dir = os.path.join(current_app.config['UPLOAD_CUSTOMERS_CV'])

        # Create the directories if they don't exist
        os.makedirs(upload_images_dir, exist_ok=True)
        os.makedirs(upload_cv_dir, exist_ok=True)
        user_id = session['user_id']
        user = Customers.query.get(user_id)

        if request.method == 'POST':
            user.fullname = request.form.get('new_fullname')
            try:
                user.birthdate = datetime.strptime(request.form.get('new_birthdate'), '%Y-%m-%d')
            except ValueError:
                flash('You have to choose a valid birthdate', 'danger')
                return redirect('/edit_my_profile')

            user.email = request.form.get('new_email')
            user.mobile = request.form.get('new_mobile')
            user.kind = request.form.get('new_kind')
            user.currentjob = request.form.get('new_currentjob')
            user.cv = request.form.get('new_cv')

            # Handle file upload for image
            if 'new_image' in request.files:
                file = request.files['new_image']

                # Check if a new image file was provided
                if file.filename:
                    # Delete the old image if it exists
                    if user.image:
                        old_image_path = os.path.join(upload_images_dir, user.image)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)

                    # Process and save the new image
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(upload_images_dir, filename))
                    new_image = filename
                    # Update the user's image field with the new image filename
                    user.image = new_image

            if 'new_cv' in request.files:
                file = request.files['new_cv']

                # Check if a new CV file was provided
                if file.filename:
                    # Delete the old CV file if it exists
                    if user.cv:
                        old_cv_path = os.path.join(upload_cv_dir, user.cv)
                        if os.path.exists(old_cv_path):
                            os.remove(old_cv_path)

                    # Process and save the new CV
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(upload_cv_dir, filename))
                    new_cv = filename
                    # Update the user's CV field with the new CV filename
                    user.cv = new_cv

            user.password = request.form.get('new_password')
            user.adress_type = request.form.get('new_adress_type')
            user.country = request.form.get('new_country')
            user.governorate = request.form.get('new_governorate')
            user.adress = request.form.get('new_adress')
            user.home_num = request.form.get('new_home_num')
            user.department_num = request.form.get('new_department_num')

            # Commit the changes to the database
            db.session.commit()

            flash('Profile updated successfully', 'success')
            return redirect('/profile')

        return render_template('edit_my_profile.html', user=user)

    # Handle cases where the user is not logged in
    flash('You must be logged in to edit your profile.', 'warning')
    return redirect('/login')



# Route to serve user images
@customer_routes.route('/download_image/<filename>')
def download_image(filename):
    return send_from_directory('static/uploads/customers/images', filename)

# Route to serve user CVs
@customer_routes.route('/download_cv/<filename>')
def download_cv(filename):
    return send_from_directory('static/uploads/customers/cv', filename)














@customer_routes.route('/apply/<int:job_id>', methods=['POST'])
def apply_job_from_company(job_id):
 if "session_ok" in session:

    customer_id = session.get('user_id')  # Assuming you store the user ID in the session
    job_id = job_id
    status = 'pending'
    note = 'didnt reviewed'
    # Check if the customer has already applied for this job
    query = customer_jobs.select().where(
        and_(customer_jobs.c.customer_id == customer_id, customer_jobs.c.job_id == job_id)
    )
    result = db.session.execute(query).fetchone()

    if result:
        flash('You have already applied for this job.')
    else:
        # If the customer has not applied for the job, insert the application
        application = customer_jobs.insert().values(customer_id=customer_id, job_id=job_id , status = status , note = note)
        db.session.execute(application)
        db.session.commit()
        flash('You have successfully applied for the job.')

    return redirect("/") 
 
 else:
     flash('You have to log in first')
     return redirect('/login')
################################ recommendations ######################
from flask import jsonify

@customer_routes.route('/recommendations')
def recommendations():
    customer_id = session.get('user_id')  # Use session.get() to avoid KeyError
    if customer_id is None:
        # Handle the case where the user is not logged in, for example, by redirecting to a login page.
        return redirect('/login')  # Replace '/login' with the actual login route

    # Assuming customer_id is the ID of the logged-in customer
    customer_skills = Skills.query.filter_by(customer_id=customer_id).all()

    # Extract skill names from customer_skills
    skill_names = [skill.skill_name for skill in customer_skills]

    # Find jobs that require any of the customer's skills
    matched_jobs = Jobs.query.filter(Jobs.skills.in_(skill_names)).all()

    # Convert matched_jobs to a list of dictionaries
    job_list = [
        {
            'id': job.id,
            'title': job.title,
            'town': job.town,
            # Add other job fields as needed
        }
        for job in matched_jobs
    ]

    # Return the job_list as JSON
    return jsonify(job_list)
'''
@customer_routes.route('/recommendations')
def recommendations():
    customer_id = session.get('user_id')  # Use session.get() to avoid KeyError
    if customer_id is None:
        # Handle the case where the user is not logged in, for example, by redirecting to a login page.
        return redirect('/login')  # Replace '/login' with the actual login route

    # Assuming customer_id is the ID of the logged-in customer
    customer_skills = Skills.query.filter_by(customer_id=customer_id).all()

    # Convert customer_skills to a list of dictionaries

    # Return the skill_list as JSON

    # Extract skill names from customer_skills
    skill_names = [skill.skill_name for skill in customer_skills]

    # Find jobs that require any of the customer's skills
    matched_jobs= Jobs.query.filter(Jobs.skills.in_(skill_names)).all()

    return jsonify(matched_jobs)
    '''
'''
    # Provide the matched job suggestions to the customer
    suggested_jobs = []
    for job in matched_jobs:
        suggested_jobs.append({
            'title': job.title,
            'description': job.job_description,
            'location': job.town,
            # Add more job details as needed
        })

    # Now, 'suggested_jobs' contains the job suggestions based on the customer's skills

    # You should return a response here, for example, render an HTML template or jsonify the data.
    # For demonstration purposes, let's return a simple JSON response.
    return jsonify({'suggested_jobs': suggested_jobs})

    '''
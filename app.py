######### START FLASK APP.py ####################
from flask import Flask, render_template, redirect, session, request, flash , jsonify  
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import or_

##### import data ####
from services.customer import Customers 
from services.job import *
from services.company import *
from services.message import *
###############
from flask_cors import CORS
import os
### separated files #####
from jobs import job_routes
from customers import customer_routes
from companies import company_routes
from messages import messages_routes

PORT = 5000
DB_FILENAME = 'database.db'
INIT_DB = True  # to create db file

def create_app():

    # create flask app
    app = Flask(__name__)

    # create database extension
    app.secret_key = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or 'sqlite:///' + DB_FILENAME

    print(app.config['SQLALCHEMY_DATABASE_URI'])

    # Set the 'UPLOAD_CUSTOMERS_IMAGES' configuration variable
    app.config['UPLOAD_CUSTOMERS_IMAGES'] = 'static/uploads/customers/images'
    
    # Set the 'UPLOAD_CUSTOMERS_IMAGES' configuration variable
    app.config['UPLOAD_CUSTOMERS_CV'] = 'static/uploads/customers/cv'
    ##### config compay logo #########
    app.config['UPLOAD_company_logo'] = 'static/uploads/company/logo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app) 

    # create flask cors extension
    CORS(app)
    with app.app_context():
        db.create_all()
    return app, db

# create flask app
app, db = create_app()
##### link separated files ##########
app.register_blueprint(job_routes)
app.register_blueprint(customer_routes)  # Adjust the prefix as needed.
app.register_blueprint(company_routes)
app.register_blueprint(messages_routes)

################################ START ROUTES ##################



@app.route('/')
def index():
    if "email_session" in session :
        email = session['email_session']
        id = session['user_id']
        img = Customers.get_customer_image_by_user_email(id=id)
    else:
        email = "Moustafa"
        img = "None"
    return render_template('index.html' , username = email , img = img)


   #######################################################################################logout##############################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/createcv')
def create_cv():
    return render_template("create_cv.html")


@app.route('/createresume')
def create_resume():
    return render_template("resume.html")

@app.route('/reg_options')
def reg_options():
    return render_template("reg_options.html")


      ##############testroutes#########
@app.route('/test')
def test_routes():
        return render_template("show_companies.html")












#########################################################to run the website####################################################################
if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')
from flask import Flask, render_template, request, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mysqldb import MySQL
from db import mysql_db, mysql_host, mysql_password, mysql_user
from flask_session import Session


#Create Flask instance
app = Flask(__name__, template_folder='template')


#Configuring the session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


#Secret key required
app.config["SECRET_KEY"] = "key"


#Add database info
app.config['MYSQL_HOST'] = mysql_host
app.config['MYSQL_USER'] = mysql_user
app.config['MYSQL_PASSWORD'] = mysql_password
app.config['MYSQL_DB'] = mysql_db

mysql = MySQL(app)



#Homepage
@app.route("/")
def home():
    # if 'loggedin' in session:
    #     return render_template('home.html')
    # else:
        return render_template('home.html')


#Login page
@app.route('/login',  methods = ['GET', 'POST'])
def login():
    #MySQL cursor
    cur1 = mysql.connection.cursor() 

    #Check that the user has inputted info
    if request.method == 'POST':

        #Store user input in variables
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if account with email exists using MySQL
        account = cur1.execute('SELECT * FROM registration_info WHERE email = %s AND password = %s', [email, password])

        if account:
            session['user_id'] = cur1.execute('SELECT user_id FROM registration_info WHERE email = %s', [email])
            session['email'] = email
            session['name'] = cur1.execute('SELECT name FROM registration_info WHERE email = %s', [email])
            session['password'] = cur1.execute('SELECT password FROM registration_info WHERE email = %s', [email])
            return redirect('/quiz_menu')
        else:
            flash('Incorrect username/password!', category = 'error')

    return render_template("login.html")



#Sign-up page. Able to GET and POST data. 
@app.route('/sign-up',  methods = ['GET', 'POST'])
def sign_up():

    #If the user posts data then store that data in the following variables.
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #Query to check if the email is in the database
        #MySQL cursor
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM registration_info WHERE email = %s",[email])
        account = cur.fetchone()

        #Flashes a warning message if the email or name is too short. Flashes a warning at the top of the page if the passwords don't match.
        #Show a confirmation message if account is successfully created.
        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstname) <2:
            flash('First name must be 2 characters or greater', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category = 'error')
        elif account:
            flash('User with email already exists. Please try another email address.', category='error')
        else:
            flash('Account created. Please sign in', category = 'success')

            #Adding the posted data to the database.
            cur.execute("INSERT INTO registration_info(name, email, password) VALUES(%s, %s, %s) ", (firstname, email, password1))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')


    return render_template("sign_up.html")



#Logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return render_template('logout.html')


#Main quiz menu
@app.route('/quiz_menu')
def quiz_menu():
    return render_template('quiz_menu.html')

if __name__ == '__main__':
    app.run(debug=True)
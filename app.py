import email
from flask import Flask, render_template, flash, request,session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, UserMixin, current_user, logout_user, login_required



#Create Flask instance. Templates rendered must be stored in a template folder
app = Flask(__name__, template_folder='template')

#secret key needed to use CSRF token
app.config['SECRET_KEY'] = 'super secret key'

#add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

#initialise db
db = SQLAlchemy(app)

#Session details
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Setting up Flask login manager for auth
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))



#Create a Model for the database
class users(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False, unique=True)
        password = db.Column(db.String(200), nullable=False)


        def __init__(self, name, email, password):
                self.name = name
                self.email = email
                self.password = password



#Create form classes
class LoginForm(FlaskForm):
        email = StringField("Email:", validators=[DataRequired()])
        password = PasswordField("Password:", validators=[DataRequired()])
        submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
        email = StringField("Email:", validators=[DataRequired()])
        name = StringField("Name:", validators=[DataRequired()])
        password1 = PasswordField("Password:", validators=[DataRequired()])
        password2 = PasswordField("Confirm Password:", validators=[DataRequired()])
        submit = SubmitField("Submit")


#Homepage
@app.route("/")
def home():
        return render_template('home.html')


#Login page
@app.route('/login',  methods = ['GET', 'POST'])
def login():
        email = None
        password = None
        name=None

        form = LoginForm()

        #Validate the form
        if form.validate_on_submit():
                email = form.email.data
                password = form.password.data

                found_user = users.query.filter_by(email=request.form['email']).first()
                hashed_password = found_user.password

                result = check_password_hash(hashed_password, password)

                if result == True:
                        login_user(found_user)
                        flash("Login successful", category='success')
                        return redirect('/index')
                                
                else:
                        flash("Wrong email/password combination. Try again.")
                        return redirect('/login')

        return render_template("login.html", email = email, password = password, form = form)

#Registration Page
@app.route('/sign_up',  methods = ['GET', 'POST'])
def sign_up():
        
        form = RegistrationForm()

        email = None
        name = None
        password1 = None
        password2 = None

        if request.method == 'POST':
                email = request.form['email']
                name = request.form['name']
                password1 = request.form['password1']
                password2 = request.form['password2']

                #Query if account with email exists
                found_user = users.query.filter_by(email=request.form['email']).first()

                #Warning statements for requirements
                if len(email) < 4:
                        flash('Email must be greater than 4 characters', category='error')
                elif len(name) <2:
                        flash('First name must be 2 characters or greater', category='error')
                elif password1 != password2:
                        flash('Passwords do not match', category = 'error')
                elif found_user:
                        flash('User with email already exists. Please try another email address.', category='error')
                else:
                        hashed_password = generate_password_hash(password1)
                        user = users(email=form.email.data, name=form.name.data, password=hashed_password)
                        db.session.add(user)
                        db.session.commit()

                        flash('Account created. Please sign in', category = 'success')

        return render_template('sign_up.html', form = form, email = email, name=name, password1 = password1, password2 = password2)



#Logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
        logout_user()

   # Redirect to login page
        return render_template('logout.html')


@app.route('/profile')
@login_required
def profile():
        return render_template('profile.html')

#Update details page
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
        form = RegistrationForm()
        name_to_update = users.query.get_or_404(id)
        if request.method == 'POST':
                name_to_update.name = form.name.data
                name_to_update.email = form.email.data
                
                try:
                        db.session.commit()
                        flash("User updated")
                        return render_template('update.html', form=form, name_to_update=name_to_update)
                except:
                        db.session.rollback()
                        flash('Error. Please try again!')
                        return render_template('update.html', form=form, name_to_update=name_to_update)

        else:
                return render_template('update.html', form=form, name_to_update=name_to_update)


        
        

@app.route('/index')
@login_required
def index():
        return render_template('index.html')










if __name__ == '__main__':
        db.create_all()
        app.run(debug=True)
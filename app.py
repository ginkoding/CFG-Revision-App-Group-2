from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__, template_folder='template')
app.secret_key = 'key'

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login',  methods = ['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

#Sign-up page. Able to GET and POST data. 
@app.route('/sign-up',  methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        #Flashes a warning message if the email or name is too short. Flashes a warning at the top of the page if the passwords don't match.
        #Show a confirmation message if account is successfully created.
        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstname) <2:
            flash('First name must be 2 characters or greater', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category = 'error')
        else:
            flash('Account created. Please sign in', category = 'success')


    return render_template("sign_up.html")

if __name__ == '__main__':
    app.run(debug=True)

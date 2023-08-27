from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dc521c243424f382543b5bd4aa769b98'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')
	
@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admain@spdd.net' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)
	
@app.route("/project/")
def project():
	return render_template('project.html')

@app.route("/about")
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True)

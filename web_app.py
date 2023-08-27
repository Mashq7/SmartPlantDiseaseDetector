from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	return "<h1>Home Page</h1>"

@app.route("/login")
def login():
	return 'Login URL'

@app.route("/register")
def register():
	return 'Register URL'
	
@app.route("/project/")
def project():
	return 'Project URL'

@app.route("/about")
def about():
	return 'about URL'

if __name__ == '__main__':
	app.run(debug=True)

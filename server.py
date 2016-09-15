# python libs
import os

# 3rd party libs
from flask import Flask, jsonify, json
from flask import request, render_template

# my libs
from models import db, connect_to_db, User

app = Flask(__name__)



@app.route("/")
def index():
	""" Homepage """

	return render_template("index.html")



@app.route("/signup", methods=['POST', 'GET'])
def register():
	""" Register new account """

	# if user filled out form (POST) process it
	# otherwise, display blank registration form
	if request.method == 'POST':

		# get user data from form
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		password = request.form['password']

		# save to db
		user = User(firstname=firstname, lastname=lastname,
				    email=email, password=password)
		db.session.add(user)
		db.session.commit()
		
		return '<h1>User successfully added</h1>'
	else:
		return render_template('register.html')



@app.route("/login", methods=['POST', 'GET'])
def login():
	""" User login """

	# if user submitted login credentials (POST) attemp login
	# otherwise, display blank login form
	if request.method == 'POST':

		# get user data
		email = request.form['email']
		password = request.form['password']

		# check user exist in db
		user = User.query.filter_by(email=email, password=password)
		
		return '<h1>User successfully logged in!</h1>'
	else:
		return render_template('login.html')



@app.route("/logout")
def logout():
	""" Log out current user """



@app.route("/profile")
def profile():
	""" Logged in user profile page """



if __name__ == "__main__":
	# 0.0.0.0 allows multiple connections to server
	connect_to_db(app, os.environ.get("DATABASE_URL"))
	DEBUG = "NO_DEBUG" not in os.environ
	DEBUG_TB_INTERCEPT_REDIRECTS = False
	PORT = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

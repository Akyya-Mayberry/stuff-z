# python libs
import os

# 3rd party libs
from flask import Flask, jsonify, json, session
from flask import request, render_template, redirect

# my libs
from models import db, connect_to_db, User, Task

app = Flask(__name__)
app.secret_key = "blaopyblaeudff"



@app.route("/")
def index():
	""" Homepage """

	# direct current loggedin users to profile
	if 'current_user' in session:
		return redirect('/profile')

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
		new_user = User(firstname=firstname, lastname=lastname,
				    email=email, password=password)

		db.session.add(new_user)
		db.session.commit()

		# add user to session and redirect to profile page
		user = User.query.filter_by(email=email).one()
		session['current_user'] = user.user_id

		return redirect('/profile')
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
		user = User.query.filter_by(email=email, password=password).one()

		# add user to session
		session['current_user'] = user.user_id
		
		return redirect('/profile')
	else:
		return render_template('login.html')



@app.route("/logout")
def logout():
	""" Log out current user """

	# Remove current user
	session.pop('current_user', None)

	return redirect('/')



@app.route("/profile")
def profile():
	""" Logged in user profile page """

	tasks = User.query.get(session['current_user']).tasks
	return render_template('profile.html', tasks=tasks)


@app.route('/add', methods=['POST', 'GET'])
def add():
	""" Add new task """

	if request.method == 'POST':
		# process
		return 'new task added'
	else:
		return render_template('add.html')



if __name__ == "__main__":
	# 0.0.0.0 allows multiple connections to server
	connect_to_db(app, os.environ.get("DATABASE_URL"))
	DEBUG = "NO_DEBUG" not in os.environ
	DEBUG_TB_INTERCEPT_REDIRECTS = False
	PORT = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

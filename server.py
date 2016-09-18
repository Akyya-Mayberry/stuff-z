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
		return redirect('/tasks')

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

		return redirect('/tasks')
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
		
		return redirect('/tasks')
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



@app.route("/tasks")
def tasks():
	""" Displays all tasks of user """

	tasks = Task.query.filter_by(user_id=session['current_user']).all()
	return render_template('tasks.html', tasks=tasks)



@app.route('/tasks/add', methods=['POST', 'GET'])
def add():
	""" Add new task """

	if request.method == 'POST':
		# process
		title = request.form['title']
		description = request.form['description']
		pic = request.form['pic']

		# add new task to db
		new_task = Task(user_id=session['current_user'], title=title, description=description)
		db.session.add(new_task)
		db.session.commit()
		
		if pic == "":
			task = Task.query.filter_by(title=title)
			task.pic = pic

		return redirect('/profile')
	else:
		return render_template('add.html')



@app.route('/tasks/<int:task_id>')
def details(task_id):
	""" Display details of specific task """

	# get task from server
	task = Task.query.get(task_id)

	return render_template('details.html', task=task)



@app.route('/tasks/<int:task_id>/edit')
def edit(task_id):
	""" Edit existing task """



@app.route('/tasks/<int:task_id>/delete')
def delete(task_id):
	""" Deletes existing task """



if __name__ == "__main__":
	# 0.0.0.0 allows multiple connections to server
	connect_to_db(app, os.environ.get("DATABASE_URL"))
	DEBUG = "NO_DEBUG" not in os.environ
	DEBUG_TB_INTERCEPT_REDIRECTS = False
	PORT = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

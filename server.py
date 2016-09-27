# python libs
import os

# 3rd party libs
from flask import Flask, jsonify, json, session
from flask import request, render_template, redirect, flash
from werkzeug import secure_filename

# my libs
from models import db, connect_to_db, User, Task

app = Flask(__name__)
app.secret_key = "blaopyblaeudff"

# images and other files uploaded
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
		try:
			user = User.query.filter_by(email=email, password=password).one()
		except:
			flash('<p>No account exist under that email, try again or <a href="/signup">signup</a> for new account.<p>')
			return redirect('/login')

		# add user to session
		session['current_user'] = user.user_id
		
		return redirect('/tasks')
	else:
		return render_template('login.html')



@app.route("/logout")
def logout():
	""" Log out current user """

	# Remove current user
	if session:
		session.pop('current_user', None)

	return redirect('/')



@app.route("/profile")
def profile():
	""" Logged in user profile page """

	user = User.query.get(session['current_user'])
	return render_template('profile.html', user=user)



@app.route("/tasks")
def tasks():
	""" Displays all tasks of user """

	user = User.query.get(session['current_user'])
	tasks = Task.query.filter_by(user_id=session['current_user'], status=False).all()
	
	return render_template('tasks.html', tasks=tasks, user=user)



@app.route('/tasks/add', methods=['POST', 'GET'])
def add():
	""" Add new task """

	# process submitted task form otherwise
	# display empty form
	if request.method == 'POST':
		
		title = request.form['title']
		description = request.form['description']
		pic = request.files['pic']
		filename = None

		# clean filename, then save to server
		if pic:
			filename = str(session["current_user"]) + "_" + secure_filename(pic.filename)
			pic.save(os.path.join(UPLOAD_FOLDER, filename))

		# add new task to db
		new_task = Task(user_id=session['current_user'], title=title, description=description, pic=filename)
		db.session.add(new_task)
		db.session.commit()

		return redirect('/tasks')
	else:
		return render_template('add.html')



@app.route('/tasks/<int:task_id>/details')
def details(task_id):
	""" Display details of specific task """

	# get task from server
	task = Task.query.get(task_id)

	return render_template('details.html', task=task)



@app.route('/tasks/<int:task_id>/edit', methods=['POST', 'GET'])
def edit(task_id):
	""" Edit existing task """

	# current task to edit
	task = Task.query.get(task_id)

	# if updating
	if request.method == 'POST':
		# get the changes
		description = request.form['description']
		pic = request.files['pic']

		# update fields
		task.description = description

		if pic:
			filename = str(session["current_user"]) + "_" + secure_filename(pic.filename)
			pic.save(os.path.join(UPLOAD_FOLDER, filename))
			task.pic = filename

		db.session.commit()
		flash('<p>Task was successfully updated!</p>')

		return redirect("/tasks/" + str(task_id) + "/details")
	else:
		return render_template('edit.html', task=task)

@app.route('/tasks/<int:task_id>/delete')
def delete(task_id):
	""" Deletes existing task """

	# get task
	task = Task.query.get(task_id)

	db.session.delete(task)
	db.session.commit()

	return redirect('/tasks')


@app.route('/tasks/<int:task_id>/completed')
def mark_complete(task_id):
	""" Mark a task as completed """

	task = Task.query.get(task_id)
	task.status = True

	db.session.commit()

	return redirect('/tasks')



if __name__ == "__main__":
	# 0.0.0.0 allows multiple connections to server
	connect_to_db(app, os.environ.get("DATABASE_URL"))
	DEBUG = "NO_DEBUG" not in os.environ
	DEBUG_TB_INTERCEPT_REDIRECTS = False
	PORT = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

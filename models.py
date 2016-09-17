""" Models and database function for Stuffz application"""

# python std libs

# third-part libs
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(30), nullable=True)
	lastname = db.Column(db.String(30), nullable=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(50), nullable=False)

	tasks = db.relationship('Task', backref='user')

	def __repr__(self):
		return "<Firstname: %s, Email: %s>" % (self.firstname, self.email)



class Task(db.Model):
	""" Tasks model for stuff to clean """

	__tablename__ = 'tasks'

	task_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
	title = db.Column(db.String)
	description = db.Column(db.Text)
	status = db.Column(db.Boolean, default=False)
	pic = db.Column(db.String, default='http://saleskiphire.co.uk/communities/1/000/001/633/941//images/7690394.jpg')

	def __repr__(self):

		return "<Title: %s Description: %s>" % (self.title, self.description)


# db connection
def connect_to_db(app, db_uri=None):
    """ Connect application to database """
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///stuffz'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    db.create_all()

# def example_data():
	
# 	# user tasks
# 	user1 = User(firstname="akyya", lastname="mayberry", email="hollywoodno@gmail.com", password="password")
	
# 	db.session.add(user1)
# 	db.session.commit()

# 	user = User.query.filter_by(email='hollywoodno@gmail.com').one()

# 	print "##user, ", user

	# task1 = Task(user_id=user.user_id, title="Reduce mail piles", description="Sort through mail, trash junk mail, store important mail"
	# )

	# task2 = Task(user_id=user.user_id, title="donate clothes", description="Sort through all clothes. Drop off unwanted clothes to Goodwill"
	# )

	# db.session.add(task1)
	# db.session.commit()
    
# if __name__ == '__main__':
# 	from app import app
# 	connect_to_db(app)
# 	print 'successfully connect to db'
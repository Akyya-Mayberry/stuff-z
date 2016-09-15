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
	email = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(50), nullable=False)

	def __repr__(self):
		return "<Firstname: %s, Email: %s>" % (self.firstname, self.email)

# db connection
def connect_to_db(app, db_uri=None):
    """ Connect application to database """
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///stuffz'
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    db.create_all()
    
if __name__ == '__main__':
	from app import app
	connect_to_db(app)
	print 'successfully connect to db'
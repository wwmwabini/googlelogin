from googlelogin import app, db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def loaduser(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	unique_id = db.Column(db.String(500), nullable=False)
	email = db.Column(db.String(500), nullable=False)
	name = db.Column(db.String(500), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
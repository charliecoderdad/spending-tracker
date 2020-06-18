from datetime import datetime
from tracker_app import db

class Expense(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.Text)	

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)    
    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"
        
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(50), unique=True, nullable=False)
	def __repr__(self):
		return f"User('{self.id}', '{self.category}')"
	

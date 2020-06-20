from datetime import datetime
from tracker_app import db

class Expense(db.Model):
	expenseId = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False)
	categoryId = db.Column(db.Integer, db.ForeignKey('category.categoryId'), nullable=False)
	spenderId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
	amount = db.Column(db.Numeric(precision=2), nullable=False)
	description = db.Column(db.Text)

	def __repr__(self):
		return f"Expense('{self.expenseId}')"

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    
    expenses = db.relationship("Expense", backref="spender")
    def __repr__(self):
        return f"User('{self.userId}', '{self.username}')"
       
class Category(db.Model):
	categoryId = db.Column(db.Integer, primary_key=True)
	expenseCategory = db.Column(db.String(50), unique=True, nullable=False)
	discretionary = db.Column(db.Boolean, nullable=False)
	
	expenses = db.relationship("Expense", backref="myCategory")
	
	def __repr__(self):
		return f"Category('{self.categoryId}', '{self.expenseCategory}')"	

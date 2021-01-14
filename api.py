

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


#init app

app=Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY']='thisissecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
db.create_all()

class Restaurant(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	public_id=db.Column(db.String(50),unique=True)
	name=db.Column(db.String(80))
	password=db.Column(db.String(80))
	admin=db.Column(db.Boolean)

class ProductCatalog(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50))
	description=db.Column(db.String(50))
	price=db.Column(db.Integer)
	status=db.Column(db.Boolean)
	restaurant_id=db.Column(db.Integer)

#Run server

if __name__=='__main__':
	app.run(debug=True)
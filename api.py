

from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import  generate_password_hash,check_password_hash
import os


#init app

app=Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY']='thisissecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


class Restaurant(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	public_id=db.Column(db.String(50),unique=True)
	name=db.Column(db.String(80))
	password=db.Column(db.String(80))
	admin=db.Column(db.Boolean)

class User(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	public_id=db.Column(db.String(50),unique=True)
	name=db.Column(db.String(50))
	password=db.Column(db.String(80))

class ProductCatalog(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50))
	description=db.Column(db.String(50))
	price=db.Column(db.Integer)
	status=db.Column(db.Boolean)
	restaurant_id=db.Column(db.Integer)

db.create_all()


@app.route('/product-catalog',methods=['POST'])
def add_product():
	return ''


@app.route('/product-catalog',methods=['GET'])
def get_all_product():
	return ''

@app.route('/product-catalog/<restaurant_id>',methods=['GET'])
def get_product_byId():
	return ''



@app.route('/restaurant',methods=['GET'])
def get_app_restaurant():
	return ''

@app.route('/user',methods=['POST'])
def create_user():
	data=request.get_json()

	hashed_password=generate_password_hash(data['password'],method='sha256')

	new_user= User(public_id=str(uuid.uuid4()),name=data['name'],password=hashed_password)
	db.session.add(new_user)
	db.session.commit()

	return jsonify({'message':'new user created'})

@app.route('/user/<user_id>',methods=['PUT'])
def update_user():
	return ''

#Run server

if __name__=='__main__':
	app.run(debug=True)
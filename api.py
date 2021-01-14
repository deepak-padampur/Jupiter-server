

from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import  generate_password_hash,check_password_hash
import datetime
import jwt
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
	data=request.get_json()

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

#create user

@app.route('/user',methods=['POST'])
def create_user():
	data=request.get_json()

	hashed_password=generate_password_hash(data['password'],method='sha256')

	new_user= User(public_id=str(uuid.uuid4()),name=data['name'],password=hashed_password)
	db.session.add(new_user)
	db.session.commit()

	return jsonify({'message':'new user created','status':'201'})

#get all user list

@app.route('/user',methods=['GET'])
def get_all_user():
	users=User.query.all()

	output=[]
	for user in users:
		user_data={}
		user_data['public_id']=user.public_id
		user_data['name']=user.name
		user_data['password']=user.password
		output.append(user_data)
	return jsonify({'users':output})

#get user by their public id number

@app.route('/user/<public_id>',methods=['GET'])
def get_user_byId(public_id):
	user=User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({'message':'No user found','status':'404'})
	user_data={}
	user_data['public_id']=user.public_id
	user_data['name']=user.name
	user_data['password']=user.password

	return jsonify({'user':user_data})

#update user data


@app.route('/user/<public_id>',methods=['PUT'])
def update_user(public_id):
	user=User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({'message':'No user found','status':'404'})

	data=request.get_json()
	user.name=data['name']
	db.session.commit()


	return jsonify({'message':'Updated details successfully'})

#delete user data

@app.route('/user/<public_id>',methods=['DELETE'])
def delete_user(public_id):
	user=User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({'message':'No user found'})


	db.session.delete(user)
	db.session.commit()

	return jsonify({'message':'User has been deleted successfully'})


#login resgitered users

@app.route('/login')
def login():
	auth=request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})

	user=User.query.filter_by(name=auth.username).first()

	if not user:
		return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})

	if check_password_hash(user.password, auth.password):
		token=jwt.encode({'public_id':user.public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
		return jsonify({'token':token})

	return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})
    

#Run server

if __name__=='__main__':
	app.run(debug=True)

from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import  generate_password_hash,check_password_hash
import datetime
import jwt
import os
from functools import wraps


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
	seller=db.Column(db.Boolean)

class User(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	public_id=db.Column(db.String(50),unique=True)
	name=db.Column(db.String(50))
	password=db.Column(db.String(80))
	seller=db.Column(db.Boolean)

class ProductCatalog(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50))
	description=db.Column(db.String(50))
	price=db.Column(db.Integer)
	status=db.Column(db.Boolean)
	restaurant_id=db.Column(db.Integer)

db.create_all()

#creating decorator for the authorization

def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token=None

		if 'x-access-token' in request.headers:
			token=request.headers['x-access-token']

		if not token:
			return jsonify({'message':'Token is missing'}),401

		try:
			data=jwt.decode(token,app.config['SECRET_KEY'],options={"verify_signature": False})
			current_user=User.query.filter_by(public_id=data['public_id']).first()	    
		except:
			return jsonify({'message':'Invalid token'}),401

		return f(current_user,*args,**kwargs)

	return decorated


#register the restaurant into theh system

@app.route('/restaurant',methods=['POST'])
def create_restaurant():
	data=request.get_json()

	hashed_password=generate_password_hash(data['password'],method='sha256')

	new_restaurant= User(public_id=str(uuid.uuid4()),name=data['name'],password=hashed_password,seller=True)
	db.session.add(new_restaurant)
	db.session.commit()

	return jsonify({'message':'new user created'}),201



@app.route('/product-catalog',methods=['POST'])
@token_required
def add_product(current_user):
	data=request.get_json()

	return ''


@app.route('/product-catalog',methods=['GET'])
def get_all_product():
	return ''

@app.route('/product-catalog/<restaurant_id>',methods=['GET'])
def get_product_byId():
	return ''



@app.route('/restaurant',methods=['GET'])
def get_all_restaurant():
	return ''

#create user

@app.route('/user',methods=['POST'])
def create_user():
	data=request.get_json()

	hashed_password=generate_password_hash(data['password'],method='sha256')

	new_user= User(public_id=str(uuid.uuid4()),name=data['name'],password=hashed_password,seller=False)
	db.session.add(new_user)
	db.session.commit()

	return jsonify({'message':'new user created','status':'201'})

#get all user list

@app.route('/user',methods=['GET'])
@token_required
def get_all_user(current_user):
	if not current_user.seller:
		return jsonify({'message':'Can not perform that function .Only sellers are allowed'}),404
	users=User.query.all()

	output=[]
	for user in users:
		user_data={}
		user_data['public_id']=user.public_id
		user_data['name']=user.name
		user_data['password']=user.password
		user_data['seller']=user.seller
		output.append(user_data)
	return jsonify({'users':output})

#get user by their public id number

@app.route('/user/<public_id>',methods=['GET'])
@token_required
def get_user_byId(current_user,public_id):
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
@token_required
def update_user(current_user,public_id):
	user=User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({'message':'No user found','status':'404'})

	data=request.get_json()
	user.name=data['name']
	db.session.commit()


	return jsonify({'message':'Updated details successfully'})

#delete user data

@app.route('/user/<public_id>',methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):
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
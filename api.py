
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

# data Model
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

class Orders(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	product_title=db.Column(db.String(50))
	price=db.Column(db.Integer)
	current_status=db.Column(db.String(10))
	restaurant_id=db.Column(db.Integer)
	product_id=db.Column(db.Integer)
	customer_id=db.Column(db.Integer)
     #This will be the public id of the customer


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
#creating decorator for restaurant
def token_required_restaurant(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token=None

		if 'x-access-token' in request.headers:
			token=request.headers['x-access-token']

		if not token:
			return jsonify({'message':'Token is missing'}),401

		try:
			data=jwt.decode(token,app.config['SECRET_KEY'],options={"verify_signature": False})
			current_restaurant=Restaurant.query.filter_by(public_id=data['public_id']).first()	
			  
		except:
			return jsonify({'message':'Invalid token'}),401

		return f(current_restaurant,*args,**kwargs)

	return decorated


#register the restaurant into theh system

@app.route('/restaurant',methods=['POST'])
def create_restaurant():
	data=request.get_json()

	hashed_password=generate_password_hash(data['password'],method='sha256')

	new_restaurant= Restaurant(public_id=str(uuid.uuid4()),name=data['name'],password=hashed_password,seller=True)
	db.session.add(new_restaurant)
	db.session.commit()

	return jsonify({'message':'Restaurant successfully registered'}),201


#adding product to the restaurant
@app.route('/product-catalog',methods=['POST'])
@token_required_restaurant
def add_product(current_restaurant):
	data=request.get_json()
   
	new_product=ProductCatalog(title=data['title'],description=data['description'],price=data['price'],status=data['status'],restaurant_id=current_restaurant.id)
	db.session.add(new_product)
	db.session.commit()



	return jsonify({"message":"product added successfully"})


@app.route('/product-catalog',methods=['GET'])
def get_all_product():
	products=ProductCatalog.query.all()

	output=[]
	for product in products:
		product_data={}
		product_data['id']=product.id
		product_data['title']=product.title
		product_data['description']=product.description
		product_data['price']=product.price
		product_data['status']=product.status
		product_data['restaurant_id']=product.restaurant_id
		output.append(product_data)
	return jsonify({'products':output})

@app.route('/product-catalog/<restaurant_id>',methods=['GET'])
def get_product_byId():
	return ''



@app.route('/restaurant',methods=['GET'])
def get_all_restaurant():
	return ''

#place order
@app.route('/place-order',methods=['POST'])
def place_order():
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

#registered restaurant login

@app.route('/login-restaurant')
def loginRestaurant():
	auth=request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})

	restaurant=Restaurant.query.filter_by(name=auth.username).first()

	if not restaurant:
		return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})

	if check_password_hash(restaurant.password, auth.password):
		token=jwt.encode({'public_id':restaurant.public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
		return jsonify({'token':token})

	return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})
    

#Run server

if __name__=='__main__':
	app.run(debug=True)
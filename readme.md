## Food Delivery System API

### Features till now

1.Restaurant can register itself with the system

2.User can create,update,delete and get profile details

3.Restaurant can add food menu (Authorized)

4.User can fetch the food menu

5.Can place order



### Features to be implemented:

1. Order status shown to user
#### Steps for running the api after cloning the repo:
```pip3 install pipenv```

```pipenv shell  ```

```pipenv install```

``python api.py``

Then you are ready to go

Running on http://127.0.0.1:5000/ 

#### You can test the api requests using postman

##### Note: You can safely delete the ```db.sqlite``` file before use

Tables

|Endpoints|REQUEST METHOD|Response|Payload|Headers
|---|---|---|---|---|
|/restaurant|POST|```{"message":"Restaurant registered successfully"}```|```{"name":"Restaurant name",password:"12345","seller":true}```| no Headers required
|/login-restaurant|GET|```{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIxYjZhMzI2ZC05NjJhLTQ4OGMtODQ2Ni0xYmU0NDUyZmVjOWYiLCJleHAiOjE2MTA2NDM0NjB9.MQoJfSxFbWweAWkfK-qAEnMzldBLF9_MiiKWKvAqhfY"}```|```{"name":"Restaurant name",password:"12345"}```|| Authorization-Basic-Authorization
|/product-catalog|POST|```{ "message": "product added successfully"}```|```{"title":"product title","description":"product desc","price":200,"status":true}```|x-access-token:response returned from above request








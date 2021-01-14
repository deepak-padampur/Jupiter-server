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

#### You can test the api requests using postman

##### Note: You can safely delete the ```db.sqlite``` file before use

Tables

|Endpoints|Payload|Headers
|---|---|--- |
|/restaurant|```{"name":"Restaurant name",password:"12345","seller":true}```| no Headers required






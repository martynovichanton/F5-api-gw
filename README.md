# F5 APIGW

## 2 projects - Django and Flask

## Traffic flow
Client -> nginx -> uwsgi -> api -> device  
Can be used withoug nginx  

## Features
1. Run multiple commands on multiple devices
2. Flexible and supports multiple devices and commands based on the required set
3. Playing with in memory ecryption of username, password and token
4. API for F5
5. Can be easily extended to use with other APIs


## Django
### Running the server
python manage.py runserver  


## Flask
### Running the server
cd API  
python f5api.py  

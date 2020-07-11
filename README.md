# BACKTRIP API

## Create your virtual python environment 
```
py -3 -m venv venv
```

## Install python dependencies
```
pip install -r requirements.txt
```

## Add python dependencies to requirements.txt
After adding your dependencies with ***pip install dependence_name*** , use the following command:
```
pip freeze > requirements.txt
```

## Database migration
After creating the ***backtrip*** database, use the following commands:
```
python manage.py db migrate
python manage.py db upgrade
```
Each time a model change or is added, use this commands to update the database. Don't forget to import the model in manage.py.

## Run the project 
The environment is managed with the environment variable `BOILERPLATE_ENV` : `prod`, `dev`, `test`. Don't forget to set it!

### Config file
```ini
[dev]
secret_key = 
files_directory = 
yelp_api_key = 
db_host = 
db_username = 
db_password = 
db_schema = 
[test]
secret_key = 
files_directory = 
yelp_api_key = 
db_host = 
db_username = 
db_password = 
db_schema = 
[prod]
secret_key = 
files_directory =
yelp_api_key = 
db_host = 
db_username = 
db_password = 
db_schema = 
```

### Development
```
python manage.py run
```

### Production
```
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 manage:app
```

## Run the tests
Don't forget to create the ***backtrip_test*** database
```
python manage.py test
```

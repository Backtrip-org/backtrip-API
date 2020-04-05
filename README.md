## BACKTRIP API
### Create your virtual python environment 
```
py -3 -m venv venv
```

###Install python dependencies
```
pip install -r requirements.txt
```

###Add python dependencies to requirements.txt
After adding your dependencies with ***pip install dependence_name*** , use the following command:
```
pip freeze > requirements.txt
```

###Database migration
After creating the ***backtrip*** database, use the following commands:
```
python manage.py db migrate
python manage.py db upgrade
```
Each time a model change or is added, use this commands to update the database. Don't forget to import the model in manage.py

###Run the project
```
python manage.py run
```

###Run the tests
Don't forget to create the ***backtrip_test*** database
```
python manage.py test
```
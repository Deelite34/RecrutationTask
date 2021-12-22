# RecrutationTask
Simple website for recrutation task purposes

# Features
- download data from external api and insert it into sqlite database using manage.py custom command.
- app/user_task/ endpoint that returns csv file generated using data from database
- tests

# Installation
create virtual environment `python -m venv venv_app`  
launch virtual environment `.\venv_app\scripts\activate`  
Install required modules `pip install -r requirements.txt`  
Create database `python manage.py makemigrations` and `python manage.py migrate`  
Run server `python manage.py runserver localhost:8080`

# Usage
Use custom command to download data from external api and to populate local sqlite db with that data  
`python manage.py add_initial_data`  
You can generate and download csv file containing that data under url  
`localhost:8080/app/user_task/`  

# Tests
Tests for different modules of the application can be ran using command:  
`python manage.py test`  

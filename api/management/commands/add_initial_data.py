import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from api.models import ApiUser, TodoItem


class Command(BaseCommand):
    help = 'Gets initial data from https://jsonplaceholder.typicode.com/ API, and inserts it ' \
           'into sqlite database. Downloaded data includes users and their assigned todos'

    def add_initial_data(self):
        """
        Downloads data from api endpoints and adds it to database.
        """

        # Get data on all users from api
        all_users_response = requests.get('https://jsonplaceholder.typicode.com/users')
        status_code = all_users_response.status_code
        if all_users_response.status_code != 200:
            raise ConnectionError(f"Users API returned status code {status_code}, and is unavailable.")
        users_json = all_users_response.json()
        user_ids = []
        for user in users_json:
            user_ids.append(user['id'])

        # Add apiusers to database
        users_to_bulk_create = []
        for user in users_json:
            external_id = user['id']
            name = user['name']
            city = user['address']['city']
            users_to_bulk_create.append(ApiUser(external_id=external_id, name=name, city=city))
        try:
            ApiUser.objects.bulk_create(users_to_bulk_create)
        except IntegrityError:
            raise IntegrityError("django.db.utils.IntegrityError: UNIQUE constraint failed: api_apiuser.external_id\n"
                                 "Users which you are attempting to add to database already exist. "
                                 "Flush database, then try again.")

        # Get data on created todos from api
        all_todos_response = requests.get('https://jsonplaceholder.typicode.com/todos')
        status_code = all_todos_response.status_code
        if status_code != 200:
            raise ConnectionError(f"Todos API returned status code {str(status_code)}, and is unavailable.")
        todos_json = all_todos_response.json()

        # Add todos to database
        todos_to_bulk_create = []
        for todo in todos_json:
            owner_id = todo['userId']
            owner = ApiUser.objects.get(external_id=owner_id)
            external_id = todo['id']
            title = todo['title']
            completed = todo['completed']
            if owner_id in user_ids:
                item = TodoItem(owner=owner, external_id=external_id, title=title, completed=completed)
                todos_to_bulk_create.append(item)
        TodoItem.objects.bulk_create(todos_to_bulk_create)

    def handle(self, *args, **options):
        """
        manage.py command, that downloads data from api and adds it to database
        used with command 'python manage.py add_initial_data'
        """
        self.add_initial_data()

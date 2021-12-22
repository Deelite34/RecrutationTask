from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from api.models import ApiUser, TodoItem

# Test class for each separate part of application is short, so there is not point in splitting them into
# separate files


class EndpointTest(TestCase):
    def test_user_task_endpoint(self):
        url = reverse('user_task')
        expected_cols = ['name', 'city', 'title', 'completed']

        response = self.client.get(url)
        headers = response.headers
        response_content = response.content.decode('utf-8')
        content_cols = response_content.split(',')
        content_cols[-1] = content_cols[-1].rstrip()  # Remove \r\n
        contains_expected_cols = all([item in content_cols for item in expected_cols])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(headers['Content-Type'], 'text/csv')
        self.assertEqual(headers['Content-Disposition'], 'attachment; filename="data.csv"')
        self.assertEqual(contains_expected_cols, True)


class CustomCommandsTest(TestCase):
    def test_add_initial_data_command(self):
        queryset_apiuser = ApiUser.objects.all()
        queryset_todoitem = TodoItem.objects.all()

        call_command('add_initial_data')
        count_apiuser = queryset_apiuser.count()
        count_todoitem = queryset_todoitem.count()

        self.assertGreaterEqual(count_apiuser, 10)
        self.assertGreaterEqual(count_todoitem, 200)


class ModelTest(TestCase):
    test_name = "testname"
    test_city = "testcity"
    external_id = 100
    test_title = "testtitle"
    test_completed = True

    def test_apiuser_to_string(self):
        test_apiuser = ApiUser.objects.create(external_id=self.external_id, name=self.test_name,
                                              city=self.test_city)
        expected_string = self.test_name

        apiuser_to_string = str(test_apiuser)

        self.assertEqual(apiuser_to_string, expected_string)

    def test_todoitem_to_string(self):
        test_apiuser = ApiUser.objects.create(external_id=self.external_id, name=self.test_name,
                                              city=self.test_city)
        test_todoitem = TodoItem.objects.create(external_id=self.external_id, owner=test_apiuser,
                                                title=self.test_title, completed=self.test_completed)
        expected_string = self.test_title

        todoitem_to_string = str(test_todoitem)

        self.assertEqual(todoitem_to_string, expected_string)

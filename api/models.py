from django.db import models


class ApiUser(models.Model):
    """
    Model representing users from external api.
    """
    # ID of user used in external api. Useful when for any reason local id of apiuser stops being
    # the same as id of user in external api
    external_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class TodoItem(models.Model):
    """
    Model representing to-do items, each assigned to specific UserData.
    """
    external_id = models.PositiveIntegerField()  # ID of todo used in external api
    owner = models.ForeignKey(ApiUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField()

    def __str__(self):
        return f"{self.title}"

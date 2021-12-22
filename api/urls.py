from django.contrib import admin
from django.urls import path

from api.views import GetCsvApiview

urlpatterns = [
    path('user_task', GetCsvApiview.as_view(), name='user_task'),

]
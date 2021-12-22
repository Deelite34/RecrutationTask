from django.contrib import admin
from .models import ApiUser, TodoItem


class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'city')


class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'owner', 'title', 'completed')


admin.site.register(ApiUser, ApiUserAdmin)
admin.site.register(TodoItem, TodoItemAdmin)

from django.contrib import admin

# Register your models here.
from .models import Appuser, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'priority', 'create_date',
                    'due_date', 'modified_date', 'status', 'created_by')
    list_filter = ('priority', 'create_date', 'status', 'created_by')
    search_fields = ('name', 'description')


@admin.register(Appuser)
class AppuserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'first_name')

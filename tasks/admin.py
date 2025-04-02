from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Поля, которые будут отображаться в списке задач
    search_fields = ('title',)  # Поиск по названию задачи
    list_filter = ('created_at',)  # Фильтр по дате создания задачи



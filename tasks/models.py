# tasks/models.py

from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)  # Название задачи
    description = models.TextField()  # Описание задачи
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания задачи

    def __str__(self):
        return self.title  # Это определяет, что будет отображаться при отображении задачи в админке


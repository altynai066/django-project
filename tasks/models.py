from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField(null=True, blank=True)  # Добавить описание
    priority = models.CharField(max_length=50, null=True, blank=True)  # Добавить приоритет
    status = models.CharField(max_length=50, null=True, blank=True)  # Добавить статус
    category = models.CharField(max_length=50, null=True, blank=True)  # Добавить категорию
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # ← вот здесь ты уже добавила null=True

    def __str__(self):
        return self.title


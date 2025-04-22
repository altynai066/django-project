from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()  # Эта строка должна быть в модели!
    created_at = models.DateTimeField(auto_now_add=True)
    
class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField(null=True, blank=True)  # Добавить описание
    priority = models.CharField(max_length=50, null=True, blank=True)  # Добавить приоритет
    status = models.CharField(max_length=50, null=True, blank=True)  # Добавить статус
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # ← вот здесь ты уже добавила null=True
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)  # Обратите внимание на поле tags

    def __str__(self):
        return self.title




# tasks/models.py
from django.db import models
from django.contrib.auth.models import User  # Не забывай импортировать модель User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField(null=True, blank=True)  # Добавить описание
    priority = models.CharField(max_length=50, null=True, blank=True)  # Добавить приоритет
    status = models.CharField(max_length=50, null=True, blank=True)  # Добавить статус
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Категория через ForeignKey
    tags = models.ManyToManyField(Tag, blank=True)  # Связь с тегами через ManyToManyField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Пользователь, который создает заметку
    password = models.CharField(max_length=128, blank=True, null=True)  # Если нужна защита паролем

    def __str__(self):
        return self.title

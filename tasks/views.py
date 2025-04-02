# views.py (в директории tasks)

from django.shortcuts import render
from .models import Task  # Импорт модели Task

def home(request):
    tasks = Task.objects.all()  # Получаем все задачи
    return render(request, 'home.html', {'tasks': tasks})  # Передаем задачи в шаблон


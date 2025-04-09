# views.py (в директории tasks)
from django.shortcuts import render
from .models import Entry  # Импорт модели Entry (не Task)
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
def home(request):
    tasks = Entry.objects.all()  # Получаем все записи (или задачи) из модели Entry
    return render(request, 'home.html', {'tasks': tasks})  # Передаем задачи в шаблон
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после регистрации
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})




# Функция для отображения страницы входа
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после успешного входа
        else:
            # Если пользователь не найден
            return render(request, 'registration/login.html', {'error': 'Invalid email or password'})
    return render(request, 'registration/login.html')

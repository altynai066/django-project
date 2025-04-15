from django.shortcuts import render
from .models import Entry  # Импорт модели Entry (не Task)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm  # Импортируйте вашу кастомную форму
from django.contrib.auth.decorators import login_required
from django.db.models import Q



def home(request):
    tasks = Entry.objects.all()  # Получаем все записи из модели Entry
    return render(request, 'home.html', {'tasks': tasks})  # Передаем задачи в шаблон


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Авторизация пользователя
            user = form.get_user()
            login(request, user)
            return redirect('home')  # После успешного логина перенаправляем на главную страницу
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем нового пользователя
            return redirect('login')  # Перенаправляем на страницу логина
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})  # Отправляем форму в шаблон



@login_required
def user_profile(request):
    # Получаем заметки пользователя
    notes = Entry.objects.filter(user=request.user)

    query = request.GET.get('q', '')
    filter_date = request.GET.get('filter_date', '')

    if query:
        notes = notes.filter(title__icontains=query)

    if filter_date:
        notes = notes.filter(created_at__date=filter_date)

    return render(request, 'user_profile.html', {
        'user': request.user,
        'notes': notes,
        'query': query,
        'filter_date': filter_date,
    })

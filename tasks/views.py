from django.shortcuts import render, redirect
from .models import Entry  # Импорт модели Entry
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, EntryForm  # Добавили EntryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    tasks = Entry.objects.all()  # Получаем все записи из модели Entry
    return render(request, 'home.html', {'tasks': tasks})  # Передаем задачи в шаблон


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


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


# ✅ Новая функция для создания заметки
@login_required
def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user  # Привязываем заметку к текущему пользователю
            entry.save()
            return redirect('user_profile')  # После создания возвращаем в профиль
    else:
        form = EntryForm()
    return render(request, 'create_entry.html', {'form': form})

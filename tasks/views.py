from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Entry, Category, Tag
from .forms import EntryForm, CustomUserCreationForm


# Главная страница с задачами
def home(request):
    tasks = Entry.objects.all()  # Получаем все записи из модели Entry
    return render(request, 'home.html', {'tasks': tasks})  # Передаем задачи в шаблон


# Вход пользователя
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


# Регистрация пользователя
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Профиль пользователя
@login_required
def user_profile(request):
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


# Создание новой записи
# Создание новой записи
@login_required
def create_entry(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            form.save_m2m()  # важно для ManyToMany
            messages.success(request, 'Заметка успешно создана!')
            return redirect('user_profile')
    else:
        form = EntryForm()

    return render(request, 'tasks/create_entry.html', {
        'form': form,
        'categories': categories,
        'tags': tags
    })


# Редактирование записи
@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(Entry, id=pk)
    if request.user != entry.user:
        return redirect('user_profile')

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заметка успешно обновлена!')  # ← Тут
            return redirect('user_profile')
    else:
        form = EntryForm(instance=entry)

    return render(request, 'edit_entry.html', {'form': form})


# Удаление записи
@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, id=pk)
    if request.user == entry.user:
        entry.delete()
        messages.success(request, 'Заметка удалена.')  # ← И вот здесь
    return redirect('user_profile')


# Детали записи с паролем
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    # Если у записи есть пароль, показываем форму для ввода пароля
    if entry.password:
        if request.method == 'POST':
            entered_password = request.POST.get('password')
            if entered_password != entry.password:
                return HttpResponseForbidden('Неверный пароль.')
        return render(request, 'tasks/entry_detail.html', {'entry': entry})

    return render(request, 'tasks/entry_detail.html', {'entry': entry})


# Фильтрация записей по категориям и тегам
def entry_list(request):
    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')

    entries = Entry.objects.all()

    if category_filter:
        entries = entries.filter(categories__name=category_filter)

    if tag_filter:
        entries = entries.filter(tags__name=tag_filter)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'tasks/entry_list.html', {'entries': entries, 'categories': categories, 'tags': tags})

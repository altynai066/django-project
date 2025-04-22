from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Entry, Category, Tag  # Импортируем модели категорий и тегов

def home(request):
    tasks = Entry.objects.all()
    return render(request, 'home.html', {'tasks': tasks})

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
def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            form.save_m2m()  # сохраняем теги (ManyToMany)
            messages.success(request, 'Заметка успешно создана!')
            return redirect('user_profile')
    else:
        form = EntryForm()
    return render(request, 'create_entry.html', {'form': form})

@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(Entry, id=pk)
    if request.user != entry.user:
        return redirect('user_profile')

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заметка успешно обновлена!')
            return redirect('user_profile')
    else:
        form = EntryForm(instance=entry)

    return render(request, 'edit_entry.html', {'form': form})

@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, id=pk)
    if request.user == entry.user:
        entry.delete()
        messages.success(request, 'Заметка удалена.')
    return redirect('user_profile')



@login_required
def user_profile(request):
    # Получаем все заметки пользователя
    notes = Entry.objects.filter(user=request.user)

    query = request.GET.get('q', '')
    filter_date = request.GET.get('filter_date', '')
    selected_category = request.GET.get('category', '')
    selected_tag = request.GET.get('tags', '')

    if query:
        notes = notes.filter(title__icontains=query)

    if filter_date:
        notes = notes.filter(created_at__date=filter_date)

    # Фильтрация по категории
    if selected_category:
        notes = notes.filter(category__name=selected_category)

    # Фильтрация по тегам
    if selected_tag:
        notes = notes.filter(tags__name=selected_tag)

    # Получаем все категории и теги для отображения в форме
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'user_profile.html', {
        'user': request.user,
        'notes': notes,
        'query': query,
        'filter_date': filter_date,
        'categories': categories,
        'tags': tags,
    })
def entries_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    entries = Entry.objects.filter(category=category)
    return render(request, 'entries_by_category.html', {'category': category, 'entries': entries})
def entries_by_tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    entries = Entry.objects.filter(tags=tag)
    return render(request, 'entries_by_tag.html', {'tag': tag, 'entries': entries})
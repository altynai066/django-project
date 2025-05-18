from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken

from .models import Entry, Category, Tag
from .forms import EntryForm, CustomUserCreationForm, EntryPasswordForm


# Главная страница с задачами
def home(request):
    tasks = Entry.objects.all()  # Получаем все записи из модели Entry
    return render(request, 'home.html', {'tasks': tasks})  # Передаем задачи в шаблон


# Вход пользователя
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print("not valid")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Регистрация пользователя
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            # Создаём устройство и токены для 2FA
            device = StaticDevice.objects.create(user=user, name='backup_codes')
            for i in range(5):
                StaticToken.objects.create(device=device, token=f'backup{i}')
            messages.success(request, 'Регистрация прошла успешно. Пожалуйста, войдите.')
            return redirect('two_factor:login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Профиль пользователя
@login_required
def user_profile(request):
    notes = Entry.objects.filter(user=request.user)

    query = request.GET.get('q', '')
    filter_date = request.GET.get('filter_date', '')
    filter_category = request.GET.get('category', '')

    if query:
        notes = notes.filter(title__icontains=query)

    if filter_date:
        notes = notes.filter(created_at__date=filter_date)

    if filter_category:
        notes = notes.filter(category__name=filter_category)

    categories = Category.objects.all()

    return render(request, 'user_profile.html', {
        'user': request.user,
        'notes': notes,
        'query': query,
        'filter_date': filter_date,
        'filter_category': filter_category,
        'categories': categories,  # <- добавили категории для шаблона
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

    return render(request, 'create_entry.html', {
        'form': form,
        'categories': categories,
        'tags': tags
    })


# Редактирование записи
@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    if entry.user != request.user:
        messages.warning(request, 'Вы не можете редактировать эту заметку.')
        return redirect('user_profile')

    # Проверка пароля
    if entry.password and not request.session.get(f'entry_passed_{entry.pk}'):
        return redirect('enter_password', pk=entry.pk)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            request.session.pop(f'entry_passed_{entry.pk}', None)
            messages.success(request, 'Заметка успешно обновлена!')
            return redirect('user_profile')
    else:
        form = EntryForm(instance=entry)
        request.session.pop(f'entry_passed_{entry.pk}', None)

    return render(request, 'edit_entry.html', {'form': form, 'entry': entry})



@login_required
def enter_password(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    if entry.user != request.user:
        messages.warning(request, 'Вы не можете получить доступ к этой заметке.')
        return redirect('user_profile')

    form = EntryPasswordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            input_password = form.cleaned_data['password']
            if input_password == entry.password:
                # Разрешаем доступ к редактированию
                request.session[f'entry_passed_{entry.pk}'] = True
                return redirect('edit_entry', pk=entry.pk)
            else:
                form.add_error('password', 'Неверный пароль.')

    return render(request, 'tasks/entry_detail.html', {
        'form': form,
        'entry': entry,
    })



# Удаление записи
@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, id=pk)
    if request.user == entry.user:
        entry.delete()
        messages.success(request, 'Заметка удалена.')  # ← И вот здесь
    return redirect('user_profile')


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

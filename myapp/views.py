from django.shortcuts import render

# Функция для главной страницы
def index(request):
    return render(request, 'index.html')  # Здесь предполагается, что у вас есть шаблон index.html

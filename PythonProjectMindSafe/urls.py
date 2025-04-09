# mysite/urls.py

# PythonProjectMindSafe/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from two_factor.urls import urlpatterns as tf_urls  # URL для двухфакторной аутентификации
from tasks import views  # Импортируем views из приложения tasks

urlpatterns = [
    path('admin/', admin.site.urls),  # URL для админки Django
    path('login/', auth_views.LoginView.as_view(), name='login'),  # URL для входа
    path('register/', views.register, name='register'),  # URL для страницы регистрации
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # Восстановление пароля
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # URL-ы для двухфакторной аутентификации
    path('two-factor/', include(tf_urls)),

    # Главная страница
    path('', views.home, name='home'),  # Добавляем маршрут для главной страницы
     path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),  # Для регистрации
    path('home/', views.home, name='home'),  # Главная страница после входа
]

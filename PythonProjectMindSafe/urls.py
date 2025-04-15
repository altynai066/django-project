from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from two_factor.urls import urlpatterns as tf_urls  # URL для двухфакторной аутентификации
from tasks import views  # Импортируем views из приложения tasks

urlpatterns = [
    # Административная панель
    path('admin/', admin.site.urls),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(), name='login'),  # URL для входа
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL для выхода
    path('register/', views.register_view, name='register'),  # URL для страницы регистрации

    # Восстановление пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Двухфакторная аутентификация
    path('two-factor/', include(tf_urls)),

    # Главная страница
    path('', views.home, name='home'),  # Главная страница для пользователей
    path('profile/', views.user_profile, name='user_profile'),
]

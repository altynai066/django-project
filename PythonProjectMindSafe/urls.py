from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Восстановление пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Двухфакторная аутентификация (рекомендуем разместить на отдельном префиксе)
    path('account/', include(tf_urls)),

    # Основное приложение
    path('', include('tasks.urls')),

   
]

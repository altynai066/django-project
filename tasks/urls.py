from django.urls import path
from . import views
from two_factor.urls import urlpatterns as tf_urls
urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('create-entry/', views.create_entry, name='create_entry'),
    path('edit-entry/<int:pk>/', views.edit_entry, name='edit_entry'),
    path('delete-entry/<int:pk>/', views.delete_entry, name='delete_entry'),
    path('profile/', views.user_profile, name='user_profile'),
    path('category/<int:category_id>/', views.entries_by_category, name='entries_by_category'),
    path('tag/<int:tag_id>/', views.entries_by_tag, name='entries_by_tag'),

]


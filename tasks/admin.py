from django.contrib import admin
from .models import Entry, Category, Tag, Task

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'status', 'category', 'created_at')
    list_filter = ('category', 'priority', 'status')
    search_fields = ('title', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)


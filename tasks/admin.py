from django.contrib import admin
from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'status', 'category', 'created_at')
    list_filter = ('category', 'priority', 'status')
    search_fields = ('title', 'description')

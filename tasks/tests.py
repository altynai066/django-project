# tasks/tests.py
from django.test import TestCase
from .models import Entry, Category, Tag

class EntryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.entry = Entry.objects.create(
            title='Test Entry',
            content='This is a test entry.',
            categories=self.category
        )
        self.entry.tags.add(self.tag)

    def test_entry_creation(self):
        """Тестируем создание заметки"""
        entry = Entry.objects.get(title='Test Entry')
        self.assertEqual(entry.content, 'This is a test entry.')
        self.assertEqual(entry.categories.name, 'Test Category')
        self.assertIn(self.tag, entry.tags.all())

    def test_entry_filtering_by_category(self):
        """Тестируем фильтрацию по категориям"""
        response = self.client.get('/tasks/?category=Test Category')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.entry, response.context['entries'])

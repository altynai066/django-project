# tasks/tests.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Entry, Category, Tag

class EntryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        self.category = Category.objects.create(name='Test Category')
        self.other_category = Category.objects.create(name='Other Category')

        self.entry1 = Entry.objects.create(
            title='Entry 1',
            content='Content 1',
            user=self.user,
            category=self.category,
        )
        self.entry2 = Entry.objects.create(
            title='Entry 2',
            content='Content 2',
            user=self.user,
            category=self.other_category,
        )

    def test_entry_creation(self):
        """Проверяет создание заметки в setUp"""
        entry = Entry.objects.get(title='Test Entry')
        self.assertEqual(entry.content, 'This is a test entry.')
        self.assertEqual(entry.category.name, 'Test Category')
        self.assertIn(self.tag, entry.tags.all())

    def test_entry_filtering_by_category(self):
        """Тестирует фильтрацию заметок по категории"""
        url = reverse('user_profile') + '?category=Test Category'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        notes = response.context['notes']
        self.assertIn(self.entry1, notes)
        self.assertNotIn(self.entry2, notes)

    def test_create_entry(self):
        """Проверка создания новой заметки"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_entry'), {
            'title': 'New Note',
            'content': 'Some content',
            'category': self.category.id,
            'tags': [self.tag.id],
        })
        self.assertEqual(response.status_code, 302)  # редирект после создания
        self.assertTrue(Entry.objects.filter(title='New Note').exists())

    def test_edit_entry_with_password(self):
        """Редактирование заметки с установленным паролем"""
        self.entry.password = 'secret'
        self.entry.save()
        self.client.force_login(self.user)

        # Подделка прохождения пароля через сессию
        session = self.client.session
        session[f'entry_passed_{self.entry.pk}'] = True
        session.save()

        response = self.client.post(reverse('edit_entry', args=[self.entry.pk]), {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'category': self.category.id,
        })
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, 'Updated Title')

    def test_edit_entry_permission_denied(self):
        """Попытка редактировать чужую заметку"""
        other_user = User.objects.create_user(username='other', password='pass')
        self.entry.user = other_user
        self.entry.save()

        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_entry', args=[self.entry.pk]))
        self.assertRedirects(response, reverse('user_profile'))

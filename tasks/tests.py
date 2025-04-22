from django.test import TestCase
from .models import Entry, Category, Tag
from django.contrib.auth.models import User

class EntryModelTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        category = Category.objects.create(name='Work')
        tag = Tag.objects.create(name='Important')

        self.entry1 = Entry.objects.create(
            title='Test Entry 1',
            content='Content 1',
            user=user,
            category=category
        )
        self.entry1.tags.add(tag)

        self.entry2 = Entry.objects.create(
            title='Test Entry 2',
            content='Content 2',
            user=user,
            category=category
        )

    def test_filter_by_category(self):
        response = self.client.get('/user-profile/', {'category': 'Work'})
        self.assertContains(response, 'Test Entry 1')
        self.assertContains(response, 'Test Entry 2')

    def test_filter_by_tag(self):
        response = self.client.get('/user-profile/', {'tags': 'Important'})
        self.assertContains(response, 'Test Entry 1')
        self.assertNotContains(response, 'Test Entry 2')


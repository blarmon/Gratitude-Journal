from django.test import TestCase
from django.contrib.auth.models import User

from journals.models import Journal

class JournalModelTestCase(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        self.user = User.objects.get_or_create(username='testuser')[0]
        self.journal = Journal.objects.create(
            user=self.user,
            title='test user blog post',
            body='first ever test gratitude journal!',
            public=True
        )

    def test_journal_basic(self):
        """
        Test the basic functionality of Journal
        """
        self.assertEqual(self.journal.title, 'test user blog post')
        self.assertEqual(self.journal.user, User.objects.get(username='testuser'))
        self.assertEqual(self.journal.body, 'first ever test gratitude journal!')


    def test_userextension_basic(self):
        """
        Test the basic functionality of Journal
        """
        self.assertEqual(self.user.userextension.slug, 'testuser')
from django.test import TestCase
from django.contrib.auth.models import User

from journals.models import Journal

class JournalModelTestCase(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

        self.journal = Journal.objects.create(
            user=User.objects.get_or_create(username='testuser')[0],
            title='test user blog post',
            body='first ever test gratitude journal!',
            public=True
        )

    def test_solo_basic(self):
        """
        Test the basic functionality of Solo
        """
        self.assertEqual(self.journal.title, 'test user blog post')
        self.assertEqual(self.journal.user, User.objects.get(username='testuser'))
        self.assertEqual(self.journal.body, 'first ever test gratitude journal!')


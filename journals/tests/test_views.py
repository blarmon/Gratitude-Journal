from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

from journals.models import Journal
from journals.views import index, explore, profile, journal_detail

class IndexViewTestCase(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def tearDown(self):
        self.client.logout()

    def test_index_view(self):
        """
        Test that the index view returns a 200 response and uses the correct template
        """
        with self.assertTemplateUsed('journals/index.html'):
            response = self.client.get(reverse('index'), follow=True)
            self.assertEqual(response.status_code, 200)


class ExploreViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_explore_view(self):
        with self.assertTemplateUsed('journals/explore.html'):
            response = self.client.get(reverse('explore'), follow=True)
            self.assertEqual(response.status_code, 200)

class ProfileViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_profile_view(self):
        with self.assertTemplateUsed('journals/profile.html'):
            response = self.client.get(reverse('profile', kwargs={'user_id': 1}))
            self.assertEqual(response.status_code, 200)

class JournalDetailViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.journal1 = Journal.objects.create(user=User.objects.get_or_create(username='testuser')[0],
                                               title='journal 1 title', body='journal 1 body', public=False,
                                               date=now() - timedelta(days=-1), id=1)

    def test_journal_detail_view(self):
        with self.assertTemplateUsed('journals/journal_detail.html'):
            response = self.client.get(reverse('journal_detail', kwargs={'journal_id': 1}))
            self.assertEqual(response.status_code, 200)
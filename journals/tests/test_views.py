from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from journals.views import index, explore, profile

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
            response = self.client.get(reverse('profile', kwargs={'user_id': 1}), follow=True)
            self.assertEqual(response.status_code, 200)
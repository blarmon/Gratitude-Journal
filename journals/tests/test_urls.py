from django.test import TestCase
from django.urls import resolve
from django.contrib.auth.models import User

from journals.views import index, explore, profile

class JournalsURLsTestCase(TestCase):

    def test_explore_url_uses_explore_view(self):
        """
        Test that the root of the site resolves to the
        correct view function
        """
        root = resolve('/explore/')
        self.assertEqual(root.func, explore)

class  JournalsURLsTestCaseAuthenticated(TestCase):

    def setUp(self):
        pass
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def tearDown(self):
        self.client.logout()

    def test_root_url_uses_index_view(self):
        """
        Test that the root of the site resolves to the
        correct view function
        """
        root = resolve('/')
        self.assertEqual(root.func, index)

    def test_profile_url_uses_profile_view(self):
        """
        Test that the root of the site resolves to the
        correct view function
        """
        root = resolve('/profile/1')
        self.assertEqual(root.func, profile)
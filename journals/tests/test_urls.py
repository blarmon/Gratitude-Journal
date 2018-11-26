from django.test import TestCase
from django.urls import resolve

from journals.views import index

class JournalsURLsTestCase(TestCase):

    def test_root_url_uses_index_view(self):
        """
        Test that the root of the site resolves to the
        correct view function
        """
        root = resolve('/')
        self.assertEqual(root.func, index)

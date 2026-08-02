from django.test import TestCase
from django.urls import reverse


class WishlistViewTests(TestCase):
    def test_wishlist_page_requires_login(self):
        response = self.client.get(reverse("wishlist"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

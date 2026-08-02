from django.test import TestCase
from django.urls import reverse


class ContactViewTests(TestCase):
    def test_contact_page_renders(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Us")

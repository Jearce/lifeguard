from django.urls import reverse
from django.test import TestCase

from payment import views

from utils.test.helpers import create_user

class EnrollmentCartTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('payment:enrollment_cart'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('payment:enrollment_cart'))
        self.assertTemplateUsed(response,'payment/enrollment_cart.html')

class LifeguardCheckout(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('payment:lifeguard_checkout'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('payment:lifeguard_checkout'))
        self.assertTemplateUsed(response,'payment/lifeguard_checkout.html')

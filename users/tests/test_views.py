from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from .. import views
from ..models import User

class SignUpViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/signup/')
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/users/signup/')
        self.assertTemplateUsed(response,'users/signup.html')

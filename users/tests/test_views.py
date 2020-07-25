from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from .. import views

class SignUpPageTest(TestCase):

    def test_uses_signup_template(self):
        response = self.client.get('/users/signup/')
        self.assertTemplateUsed(response,'users/signup.html')

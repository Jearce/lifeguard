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

class LogInViewTest(TestCase):

    def setUp(self):
        self.credentials = {'email':'test@example.com', 'password':'2dhd7!42'}
        User.objects.create_user(**self.credentials)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/users/login/')
        self.assertTemplateUsed(response,'users/login.html')

    def test_login(self):
        user_login = self.client.login(**self.credentials)
        self.assertTrue(user_login)


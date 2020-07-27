from django.urls import resolve
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .. import views
from ..models import User

class SignUpViewTest(TestCase):

    def setUp(self):
        self.credentials = {'email':'test@example.com', 'password1':'2dhd7!42','password2':'2dhd7!42'}

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response,'users/signup.html')

    def test_signup(self):
        response = self.client.post(reverse('signup'),data=self.credentials)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(),1)

    def test_redirect_after_signup(self):
        response = self.client.post(reverse('signup'),data=self.credentials)
        self.assertRedirects(response,reverse('dashboard'))


class LogInViewTest(TestCase):

    def setUp(self):
        self.credentials = {'email':'test@example.com', 'password':'2dhd7!42'}
        User.objects.create_user(**self.credentials)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response,'users/login.html')

    def test_login(self):
        user_login = self.client.login(**self.credentials)
        self.assertTrue(user_login)

    def test_redirect_after_login(self):
        response = self.client.post(
            reverse('login'),
            data={'username':self.credentials['email'],
                'password':self.credentials['password']})
        self.assertRedirects(response,reverse('dashboard'))




class DashboardViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/users/dashboard/')
        self.assertTemplateUsed(response,'users/dashboard.html')

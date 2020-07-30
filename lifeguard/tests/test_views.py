from django.urls import resolve
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .. import views
from users.models import User

class HomeViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response,'home.html')

class ContactUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com',password='sdfh328j!')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('contact_information',kwargs={'pk':self.user.id}))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('contact_information',kwargs={'pk':self.user.id}))
        self.assertTemplateUsed(response,'contact_information_form.html')

    def test_contact_information_update(self):
        user = User.objects.create(email='test@example.com',password='sdfh328j!')
        contact_information = {
            "first_name": "John",
            "last_name": "Doe",
            "phone":"712 434 2348",
            "dob":"6/9/2000"
        }
        response = self.client.post(reverse('contact_information',kwargs={'pk':self.user.id}),data=contact_information)
        self.assertEqual(response.status_code,302)
        user.refresh_from_db()
        self.assertEqual(user.first_name,'John')


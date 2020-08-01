from django.urls import resolve
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .. import views
from users.models import User
from ..models import EmergencyContact

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
        self.assertTemplateUsed(response,'lifeguard/contact_information_form.html')

    def test_contact_information_update(self):
        contact_information = {
            "email":self.user.email,
            "first_name": "John",
            "last_name": "Doe",
            "phone":"712 434 2348",
            "dob":"2000-06-09"
        }
        response = self.client.post(reverse('contact_information',kwargs={'pk':self.user.id}),contact_information)
        self.assertEqual(response.status_code,302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name,'John')
        self.assertRedirects(response,reverse('emergency_contact'))

class EmergencyContactCreateTest(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'sdfh328j!'
        self.user = User.objects.create_user(email=self.email,password=self.password)
        self.response = self.client.get(reverse('emergency_contact'))

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'lifeguard/emergency_contact_form.html')

    def test_emergency_contact_create(self):
        user_login = self.client.login(email=self.email,password=self.password)
        self.assertTrue(user_login)
        emergency_contact = {
            "name":"Mary",
            "relationship":"mom",
            "phone":"712 434 2348"
        }
        response = self.client.post(reverse('emergency_contact'),emergency_contact)
        self.assertEqual(response.status_code,302)

        em_contacts = EmergencyContact.objects.filter(user=self.user)
        for em_contact in em_contacts:
            self.assertEqual(em_contact.user.email,self.user.email)

        self.assertRedirects(response,reverse('address'))

class AddressCreateTest(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'sdfh328j!'
        self.user = User.objects.create_user(email=self.email,password=self.password)
        self.response = self.client.get(reverse('address'))

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'lifeguard/address_form.html')

    def test_address_create(self):
        user_login = self.client.login(email=self.email,password=self.password)
        self.assertTrue(user_login)
        address = {
            "street1":"123 Main St",
            "stree2":"",
            "city":"San Diego",
            "state":"CA",
            "zip":"94103"
        }
        response = self.client.post(reverse('address'),address)
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.user.address_set.count(),1)

class LifeguardCreateTest(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'sdfh328j!'
        self.user = User.objects.create_user(email=self.email,password=self.password)
        self.response = self.client.get(reverse('lifeguard_create'))

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'lifeguard/lifeguard_form.html')






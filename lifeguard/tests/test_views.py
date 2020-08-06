from django.urls import resolve
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .. import views
from users.models import User
from ..models import LifeguardClass,Enroll,Lifeguard

class BaseUserSetUp(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'sdfh328j!'
        self.user = User.objects.create_user(email=self.email,password=self.password)

class HomeViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response,'home.html')

class LifeguardCreateTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.user_login = self.client.login(email=self.email,password=self.password)
        self.lifeguard_data = {
            "already_certified":"N",
            "wants_to_work_for_company":"Y",
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('lifeguard:create'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('lifeguard:create'))
        self.assertTemplateUsed(response,'lifeguard/lifeguard_form.html')

    def test_lifeguard_create(self):
        response = self.client.post(reverse('lifeguard:create'),self.lifeguard_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('lifeguard:classes'))

    def test_lifeguard_update(self):
        #user is already a lifeguard
        Lifeguard.objects.create(user=self.user,**self.lifeguard_data)

        updated_lifeguard = self.lifeguard_data.copy()
        updated_lifeguard["already_certified"]  = "Y"

        response = self.client.post(reverse('lifeguard:create'),updated_lifeguard)
        self.assertEqual(Lifeguard.objects.count(),1)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('lifeguard:classes'))

    def test_correct_redirect_for_already_certified_lifeguard(self):
        updated_lifeguard = self.lifeguard_data.copy()
        updated_lifeguard["already_certified"]  = "Y"
        response = self.client.post(reverse('lifeguard:create'),self.lifeguard_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('lifeguard:already_certified'))

class LifeguardAlreadyCertifiedTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.user_login = self.client.login(email=self.email,password=self.password)
        self.lifeguard_data = {
            "already_certified":"Y",
            "wants_to_work_for_company":"Y",
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        Lifeguard.objects.create(user=self.user,**self.lifeguard_data)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('lifeguard:already_certified'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('lifeguard:already_certified'))
        self.assertTemplateUsed(response,'lifeguard/already_certified_form.html')

class LifeguardClassesTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('lifeguard:classes'))
        self.lifeguard_data = {
            "already_certified":"N",
            "wants_to_work_for_company":"Y",
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'lifeguard/classes.html')

    def test_can_enroll_in_class(self):
        user_login = self.client.login(email=self.email, password=self.password)
        Lifeguard.objects.create(user=self.user,**self.lifeguard_data)
        class1 = {
            "course":"Review",
            "start_date":"2020-8-28 14:30:59",
            "end_date":"2020-9-8 14:30:59",
            "cost":120.23,
            "employee_cost":50.50
        }
        class2 = {
            "course":"Lifeguard",
            "start_date":"2020-8-28 14:30:59",
            "end_date":"2020-9-8 14:30:59",
            "cost":120.23,
            "employee_cost":50.50
        }
        LifeguardClass.objects.bulk_create(
            [LifeguardClass(**class1),
             LifeguardClass(**class2)]
        )
        classes = LifeguardClass.objects.all()
        response = self.client.post(reverse('lifeguard:classes',kwargs={'pk':classes[0].id}))
        self.assertEqual(response.status_code,302)
        self.assertEqual(Enroll.objects.all().count(),1)
        self.assertRedirects(response,reverse('lifeguard:payment'))

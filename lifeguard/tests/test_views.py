from django.urls import resolve
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .. import views
from users.models import User
from ..models import EmergencyContact,LifeguardClass,Enroll,Lifeguard

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
        self.assertRedirects(response,reverse('emergency_contact_create'))

class BaseUserSetUp(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'sdfh328j!'
        self.user = User.objects.create_user(email=self.email,password=self.password)

class EmergencyContactCreateTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('emergency_contact_create'))

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'lifeguard/emergency_contact_form.html')

    def test_emergency_contact_create(self):
        user_login = self.client.login(email=self.email,password=self.password)
        self.assertTrue(user_login)
        emergency_contact = {
            "form-TOTAL_FORMS":2,
            "form-INITIAL_FORMS":'0',
            'form-MAX_NUM_FORMS':'',
            "form-0-name":"Mary",
            "form-0-relationship":"mom",
            "form-0-phone":"712 434 2348",
            "form-1-name":"Jerry",
            "form-1-relationship":"dad",
            "form-1-phone":"712 434 2348"

        }
        response = self.client.post(reverse('emergency_contact_create'),emergency_contact)
        self.assertEqual(response.status_code,302)

        em_contacts = EmergencyContact.objects.filter(user=self.user)
        self.assertEqual(em_contacts.count(),2)

        self.assertRedirects(response,reverse('address'))

class EmergencyContactUpdateTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('emergency_contact_update'))
        emergency_contacts = [
            {
                "name":"Mary",
                "relationship":"mom",
                "phone":"712 434 2348"
            },
            {
                "name":"Jerry",
                "relationship":"dad",
                "phone":"712 434 2348"
            }
        ]

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'lifeguard/emergency_contact_form.html')

    def test_emergency_contact_create(self):
        user_login = self.client.login(email=self.email,password=self.password)
        self.assertTrue(user_login)

class AddressCreateTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
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

class LifeguardCreateTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('lifeguard_create'))

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,'lifeguard/lifeguard_form.html')

    def test_new_lifeguard_creation_and_wants_to_work(self):
        user_login = self.client.login(email=self.email,password=self.password)
        lifeguard_data = {
            "already_certified":"N",
            "wants_to_work_for_company":"Y",
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        response = self.client.post(reverse('lifeguard_create'),lifeguard_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('classes'))

class LifeguardClassesTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('classes'))
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
        response = self.client.post(reverse('classes',kwargs={'pk':classes[0].id}))
        self.assertEqual(response.status_code,302)
        self.assertEqual(Enroll.objects.all().count(),1)
        self.assertRedirects(response,reverse('payment'))

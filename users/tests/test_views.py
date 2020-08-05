from django.urls import resolve
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .. import views
from ..models import User,EmergencyContact,Address
from ..forms import EmergencyContactInlineFormSet

class SignUpViewTest(TestCase):

    def setUp(self):
        self.credentials = {'email':'test@example.com', 'password1':'2dhd7!42','password2':'2dhd7!42'}

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:signup'))
        self.assertTemplateUsed(response,'users/signup.html')

    def test_signup(self):
        response = self.client.post(reverse('users:signup'),data=self.credentials)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(),1)

    def test_redirect_after_signup(self):
        response = self.client.post(reverse('users:signup'),data=self.credentials)
        self.assertRedirects(response,reverse('users:dashboard'))

class LogInViewTest(TestCase):

    def setUp(self):
        self.credentials = {'email':'test@example.com', 'password':'2dhd7!42'}
        User.objects.create_user(**self.credentials)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response,'users/login.html')

    def test_login(self):
        user_login = self.client.login(**self.credentials)
        self.assertTrue(user_login)

    def test_redirect_after_login(self):
        response = self.client.post(
            reverse('users:login'),
            data={'username':self.credentials['email'],
                  'password':self.credentials['password']})
        self.assertRedirects(response,reverse('users:dashboard'))

class DashboardViewTest(TestCase):

    def setUp(self):
        self.credentials = {'email':'test@example.com', 'password':'2dhd7!42'}
        user = User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/users/dashboard/')
        self.assertTemplateUsed(response,'users/dashboard.html')

class BaseUserSetUp(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'sdfh328j!'
        self.user = User.objects.create_user(email=self.email,password=self.password)

class ContactUpdateViewTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.user_login = self.client.login(email=self.email,password=self.password)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('users:contact_information',kwargs={'pk':self.user.id}))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:contact_information',kwargs={'pk':self.user.id}))
        self.assertTemplateUsed(response,'users/contact_information_form.html')

    def test_contact_information_update(self):
        contact_information = {
            "email":self.user.email,
            "first_name": "John",
            "last_name": "Doe",
            "phone":"712 434 2348",
            "dob":"2000-06-09"
        }
        response = self.client.post(reverse('users:contact_information',kwargs={'pk':self.user.id}),contact_information)
        self.assertEqual(response.status_code,302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name,'John')
        self.assertRedirects(response,reverse('users:emergency_contact'))

class EmergencyContactCreateOrUpdateTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.user_login = self.client.login(email=self.email,password=self.password)
        self.emergency_contacts = [
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
        response = self.client.get(reverse('users:emergency_contact'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:emergency_contact'))
        self.assertTemplateUsed(response,'users/emergency_contact_form.html')

    def test_emergency_contact_update(self):
        new_em_contacts = {
            'emergencycontact_set-TOTAL_FORMS': '2',
            'emergencycontact_set-INITIAL_FORMS': '1',
            'emergencycontact_set-MIN_NUM_FORMS': '0',
            'emergencycontact_set-MAX_NUM_FORMS': '2',
            'emergencycontact_set-0-name': 'Mary Jane',
            'emergencycontact_set-0-relationship': 'Mom',
            'emergencycontact_set-0-phone': '712 526 2555',
            'emergencycontact_set-0-user': self.user.id,
            'emergencycontact_set-0-id': '1',
            'emergencycontact_set-1-name': 'Larry Deems',
            'emergencycontact_set-1-relationship': 'Brother',
            'emergencycontact_set-1-phone': '715 8452 1235',
            'emergencycontact_set-1-id': '',
            'emergencycontact_set-1-user':self.user.id,
        }

        #user already created emergency contact (em)
        EmergencyContact.objects.create(user=self.user,**self.emergency_contacts[0])
        self.assertEqual(EmergencyContact.objects.filter(user=self.user).count(),1)

        #user updates the current em and adds another em
        response = self.client.post(reverse('users:emergency_contact'),new_em_contacts)
        self.assertEqual(response.status_code,302)
        self.assertEqual(EmergencyContact.objects.filter(user=self.user).count(),2)

    def test_emergency_contact_create(self):
        em_contacts = {
            'emergencycontact_set-TOTAL_FORMS': '2',
            'emergencycontact_set-INITIAL_FORMS': '0',
            'emergencycontact_set-MIN_NUM_FORMS': '0',
            'emergencycontact_set-MAX_NUM_FORMS': '2',
            'emergencycontact_set-0-name': 'Mary Jane',
            'emergencycontact_set-0-relationship': 'Mom',
            'emergencycontact_set-0-phone': '712 526 2555',
            'emergencycontact_set-0-user': self.user.id,
            'emergencycontact_set-0-id': '',
            'emergencycontact_set-1-name': 'Larry Deems',
            'emergencycontact_set-1-relationship': 'Brother',
            'emergencycontact_set-1-phone': '715 8452 1235',
            'emergencycontact_set-1-id': '',
            'emergencycontact_set-1-user':self.user.id,
        }
        response = self.client.post(reverse('users:emergency_contact'),em_contacts)
        self.assertEqual(response.status_code,302)
        self.assertEqual(EmergencyContact.objects.filter(user=self.user).count(),2)

class AddressCreateOrUpdateTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.current_address = {
            "street1":"123 Main St",
            "street2":"",
            "city":"San Diego",
            "state":"CA",
            "zip":"94103"
        }
        self.new_address = {
            "street1":"123 Main St",
            "street2":"Apt 1",
            "city":"San Diego",
            "state":"CA",
            "zip":"94103"
        }
        self.user_login = self.client.login(email=self.email,password=self.password)
        self.assertTrue(self.user_login)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('users:address'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:address'))
        self.assertTemplateUsed(response,'users/address_form.html')

    def test_address_create(self):
        response = self.client.post(reverse('users:address'),self.current_address)
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.user.address_set.count(),1)

    def test_address_update(self):
        Address.objects.create(user=self.user,**self.current_address)
        self.assertEqual(self.user.address_set.count(),1)
        response = self.client.post(reverse('users:address'),self.new_address)
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.user.address_set.count(),1)

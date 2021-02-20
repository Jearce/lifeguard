from django.urls import resolve
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from users import views
from users.models import User,EmergencyContact,Address
from users.forms import EmergencyContactInlineFormSet

from utils.test.helpers import InlineFormsetManagmentFactory


class BaseUserSetUp(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'sdfh328j!'
        self.credentials = {
            'first_name':'Larry',
            'last_name':'John',
            'dob':'1995-06-09',
            'phone':'121 382 8292',
        }
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            **self.credentials
        )
        self.client.login(email=self.email,password=self.password)


class SignUpViewTest(TestCase):

    def setUp(self):
        self.credentials = {
            'email':'test@example.com',
            'first_name':'Larry',
            'last_name':'John',
            'dob':'1995-06-09',
            'phone':'121 382 8292',
            'street1':"123 Main St",
            'state':'Oregon',
            'city':'Portland',
            'zip':'97035',
            'password1':'2dhd7!42',
            'password2':'2dhd7!42'
        }

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
        self.assertEqual(Address.objects.count(),1)

    def test_redirect_after_signup(self):
        response = self.client.post(reverse('users:signup'),data=self.credentials)
        self.assertRedirects(response,reverse('users:emergency_contact'))

class LogInViewTest(BaseUserSetUp):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response,'users/login.html')

    def test_login(self):
        user_login = self.client.login(email=self.email,password=self.password)
        self.assertTrue(user_login)

    def test_redirect_after_login(self):
        response = self.client.post(
            reverse('users:login'),
            data={'username':self.email,
                  'password':self.password})
        self.assertRedirects(response,reverse('users:dashboard'))

class DashboardViewTest(BaseUserSetUp):

    def setUp(self):
        super().setUp()
        self.client.login(email=self.email,password=self.password)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/users/dashboard/')
        self.assertTemplateUsed(response,'users/dashboard.html')


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
        self.emergency_contacts_to_create = [
            {
                "name":"Mary Jane",
                "relationship":"Mom",
                "phone":"713 526 2555",
                "user":self.user.id,
                "id":''
            },
            {
                "name":"Larry Deems",
                "relationship":"Brother",
                "phone":"713 343 2555",
                "user":self.user.id,
                "id":''
            }
        ]
        self.emergency_contacts_to_update = [
            {
                "name":"Mary Jane",
                "relationship":"Mom",
                "phone":"713 888 2555",
                "user":self.user.id,
                "id":'1'
            },
            {
                "name":"Larry Deems",
                "relationship":"Brother",
                "phone":"713 343 2555",
                "user":self.user.id,
                "id":''
            }
        ]


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('users:emergency_contact'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:emergency_contact'))
        self.assertTemplateUsed(response,'users/emergency_contact_form.html')

    def test_emergency_contact_update(self):
        #user already created emergency contact
        em = EmergencyContact.objects.create(user=self.user,**self.emergency_contacts[0])
        self.assertEqual(EmergencyContact.objects.filter(user=self.user).count(),1)

        self.emergency_contacts_to_update[0].update({'id': em.id})
        management_factory = InlineFormsetManagmentFactory(
                    EmergencyContactInlineFormSet,
                    extra=2,
                    initial=1,
                    min_num=0,
                    max_num=2,
                    records=self.emergency_contacts_to_update
                )
        new_em_contacts = management_factory.create_management_form()

        #user updates the current em and adds another em
        response = self.client.post(reverse('users:emergency_contact'),new_em_contacts)
        self.assertEqual(response.status_code,302)
        self.assertEqual(EmergencyContact.objects.filter(user=self.user).count(),2)

    def test_emergency_contact_create(self):
                #Emergency Contact
        management_factory = InlineFormsetManagmentFactory(
            EmergencyContactInlineFormSet,
            extra=2,
            initial=0,
            min_num=0,
            max_num=2,
            records=self.emergency_contacts_to_create
        )

        em_contacts = management_factory.create_management_form()
        response = self.client.post(reverse('users:emergency_contact'),em_contacts)
        self.assertEqual(response.status_code,302)
        self.assertEqual(EmergencyContact.objects.filter(user=self.user).count(),2)

    def test_redirect_after_form_submit(self):
        #Emergency Contact
        management_factory = InlineFormsetManagmentFactory(
            EmergencyContactInlineFormSet,
            extra=2,
            initial=0,
            min_num=0,
            max_num=2,
            records=self.emergency_contacts_to_create
        )

        em_contacts = management_factory.create_management_form()
        response = self.client.post(reverse('users:emergency_contact'),em_contacts)
        self.assertRedirects(response,reverse('users:dashboard'))

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


class AdminPanelViewTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.user.is_superuser = True
        self.user.save()


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('users:admin_panel'))
        self.assertEqual(response.status_code,200)


    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:admin_panel'))
        self.assertTemplateUsed(response,'users/admin_panel.html')


class AdminAddUserViewTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.user.is_superuser = True
        self.user.save()

        self.credentials = {
            'email':'another@example.com',
            'first_name':'Larry',
            'last_name':'John',
            'dob':'1995-06-09',
            'phone':'121 382 8292',
            'street1':"123 Main St",
            'state':'Oregon',
            'city':'Portland',
            'zip':'97035',
            'password1':'2dhd7!42',
            'password2':'2dhd7!42'
        }


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('users:admin_add_user'))
        self.assertEqual(response.status_code,200)


    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users:admin_add_user'))
        self.assertTemplateUsed(response,'users/admin_add_user.html')


    def test_can_add_user(self):
        response = self.client.post(reverse('users:admin_add_user'),data=self.credentials)
        users = User.objects.all()
        self.assertEqual(users.count(),2)
        self.assertEqual(Address.objects.count(),1)


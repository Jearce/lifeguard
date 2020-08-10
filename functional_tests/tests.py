import time
import unittest
import re

from django.test import LiveServerTestCase
from django.core import mail
from django.urls import reverse,reverse_lazy

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from users.models import User
from lifeguard.models import LifeguardClass,Enroll

class BaseTestFixture(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.credentials = {
            'username':'test@example.com',
            'password':'u7efd!hd',
            'first_name':'John',
            'last_name' : 'Doe',
            'phone' : '713 434 4564',
            'dob' : '2000-06-09',
        }
        self.address = {
           'street1' : "123 Main St",
           'city' : "San Diego",
           'state' : "CA",
           'zip_code' : "94103"
        }
        self.emergency_contact = {
            'name':'Mary Jane',
            'relationship':'Mom',
            'phone':'832 283 2834',
        }
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


    def tearDown(self):
        self.browser.quit()

    def sign_up(self):
        #select account opitions to get to sign up link
        self.browser.find_element_by_class_name('navbar-toggler').click()
        self.browser.implicitly_wait(5)
        self.browser.find_element_by_id('navbarDropdown').click()

        self.browser.find_element_by_id('id_signup').click()
        self.assertIn('signup',self.browser.current_url)

        email_input = self.browser.find_element_by_id('id_email')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')

        email = self.credentials['username']
        password = self.credentials['password']

        email_input.send_keys(email)
        password1_input.send_keys(password)
        password2_input.send_keys(password)

        self.browser.find_element_by_id('signup-form').submit()
        self.assertIn('dashboard',self.browser.current_url)

    def fill_out_contact_information(self):
        first_name = self.credentials['first_name']
        last_name =  self.credentials['last_name']
        phone = self.credentials['phone']
        dob = self.credentials['dob']
        self.browser.find_element_by_id('id_first_name').send_keys(first_name)
        self.browser.find_element_by_id('id_last_name').send_keys(last_name)
        self.browser.find_element_by_id('id_phone').send_keys(phone)
        self.browser.find_element_by_id('id_dob').send_keys(dob)
        self.browser.find_element_by_id('contact_information_form').submit()
        self.assertIn('emergency-contact/',self.browser.current_url)


    def fill_out_emergency_contact(self):
        name = self.emergency_contact["name"]
        relationship = self.emergency_contact["relationship"]
        phone = self.emergency_contact["phone"]
        self.browser.find_element_by_id('id_emergencycontact_set-0-name').send_keys(name)
        self.browser.find_element_by_id('id_emergencycontact_set-0-relationship').send_keys(relationship)
        self.browser.find_element_by_id('id_emergencycontact_set-0-phone').send_keys(phone)
        self.browser.find_element_by_id('emergency_contact_form').submit()
        self.assertIn('address/',self.browser.current_url)

    def fill_out_address_form(self):
        street1 = self.address['street1']
        city = self.address['city']
        state = self.address['state']
        zip_code = self.address['zip_code']
        self.browser.find_element_by_id('id_street1').send_keys(street1)
        self.browser.find_element_by_id('id_city').send_keys(city)
        self.browser.find_element_by_id('id_state').send_keys(state)
        self.browser.find_element_by_id('id_zip').send_keys(zip_code)
        self.browser.find_element_by_id('address_form').submit()
        self.assertIn('lifeguard/create/',self.browser.current_url)

    def fill_employee_form(self):
        self.browser.find_element_by_id('employee_form').submit()
        self.assertIn('employee/education/',self.browser.current_url)


    def register_new_lifeguard_who_wants_to_work(self):
        #user is a new lifeguard
        already_certified = "N"
        #and wants to work as a lifeguard
        wants_to_work_for_company = "Y"
        payment_agreement = True
        payment_agreement_signature = "Larry Jones"
        no_refunds_agreement = True
        electronic_signature = "Larry Jones"
        self.browser.find_element_by_id('id_already_certified').send_keys(already_certified)
        self.browser.find_element_by_id('id_wants_to_work_for_company').send_keys(wants_to_work_for_company)
        self.browser.find_element_by_id('id_payment_agreement').send_keys(payment_agreement)
        self.browser.find_element_by_id('id_payment_agreement_signature').send_keys(payment_agreement_signature)
        self.browser.find_element_by_id('id_no_refunds_agreement').send_keys(no_refunds_agreement)
        self.browser.find_element_by_id('id_electronic_signature').send_keys(electronic_signature)
        self.browser.find_element_by_id('lifeguard_form').submit()

class SignUpTest(BaseTestFixture):

    def test_sign_up_and_registers_as_new_lifeguard(self):
        #user lands on homepage
        self.browser.get(self.live_server_url)
        self.assertIn('Home',self.browser.title)

        #signs up and is taken to dashboard
        self.sign_up()

        #clicks on LG registration link
        self.browser.find_element_by_id('id_lifeguard_registration').click()
        #is taken to the contact information form
        self.assertIn('contact-information/',self.browser.current_url)
        #and fills out form
        self.fill_out_contact_information()

        #proceeds to emergency contact form
        #and fills out form
        self.fill_out_emergency_contact()

        #next fill out address form
        self.fill_out_address_form()

        #proceeds to LG form and fills form
        self.register_new_lifeguard_who_wants_to_work()
        #is taken to employee registration page
        self.assertIn('employee/create/',self.browser.current_url)
        self.fill_employee_form()

        #picks a class to attend
        #enrollment_btns = self.browser.find_elements_by_name('enroll-btn')
        #enrollment_btns[0].submit()
        #self.assertEqual(Enroll.objects.count(),1)

        #makes payment
        self.fail("Finish payment")

        #redirect to dashboard

class LogInTest(BaseTestFixture):

    def setUp(self):
        super().setUp()
        User.objects.create_user(
            email=self.credentials['username'],
            password=self.credentials['password']
        )

    def test_at_login_page(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        self.assertIn('Login',self.browser.title)

    def test_login(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys(self.credentials['username'])
        password.send_keys(self.credentials['password'])
        self.browser.find_element_by_id('login-form').submit()
        #check user is redirected to dashboard on successful login
        self.assertIn('dashboard',self.browser.current_url)

class PasswordResetTest(BaseTestFixture):

    def setUp(self):
        super().setUp()
        #user already has an account
        self.user = User.objects.create_user(
            email=self.credentials['username'],
            password=self.credentials['password']
        )

    def test_at_password_reset_page(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/password_reset/'))
        self.assertIn('Password Reset',self.browser.title)

    def test_can_reset_password(self):
        #user forgot their password
        self.browser.get('%s%s' % (self.live_server_url,'/users/password_reset/'))
        self.browser.find_element_by_id('id_email').send_keys(self.user.email)
        self.browser.find_element_by_id('forgot-password-form').submit()
        self.assertIn('done',self.browser.current_url)

        #user recieved email for password reset
        self.assertEqual(len(mail.outbox),1)

        #user goes to password reset url
        self.assertIn('reset',mail.outbox[0].subject)
        match = re.search(r'http:\/\/[\w]+:[\w]+\/users\/password_reset_confirm\/[\w]+\/.+\/',mail.outbox[0].body)
        self.assertTrue(match)
        reset_url = match[0]
        self.browser.get(reset_url)
        self.assertIn('Change password',self.browser.page_source)

        #user resets password
        new_password = 'newPasswordTest123!'
        self.browser.find_element_by_id('id_new_password1').send_keys(new_password)
        self.browser.find_element_by_id('id_new_password2').send_keys(new_password)
        self.browser.find_element_by_id('change-password-form').submit()
        self.assertIn('complete',self.browser.current_url)

        #user gets redirected to login page after resetting password
        self.browser.find_element_by_id('id_login').click()
        self.assertIn('login',self.browser.current_url)

        #user logs in with new password
        self.browser.find_element_by_id('id_username').send_keys(self.user.email)
        self.browser.find_element_by_id('id_password').send_keys(new_password)
        self.browser.find_element_by_id('login-form').submit()
        self.assertIn('dashboard',self.browser.current_url)

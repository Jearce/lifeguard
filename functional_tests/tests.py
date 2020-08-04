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

    def tearDown(self):
        self.browser.quit()

class SignUpToLifeguardRegistrationTest(BaseTestFixture):

    def setUp(self):
        super().setUp()
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

    def test_sign_up_and_registers_as_new_lifeguard(self):
        #user lands on homepage
        self.browser.get('%s%s' % (self.live_server_url,'/home'))
        self.assertIn('Home',self.browser.title)

        #Clicks on account dropdown
        self.browser.find_element_by_id('navbarDropdown').click()

        #Clicks on sign up option
        self.browser.find_element_by_id('id_signup').click()
        self.assertIn('signup',self.browser.current_url)

        #signs up
        self.sign_up()

        #redirected to dashboard on successful sign up
        self.assertIn('dashboard',self.browser.current_url)

        #clicks on LG registration link
        self.browser.find_element_by_id('id_lifeguard_registration').click()

        #is taken to the contact information form
        base = 'lifeguard-registration/'
        self.assertIn(base+'contact-information/',self.browser.current_url)

        #fills out contact information form
        self.fill_out_contact_information()
        #proceeds to emergency contact form
        self.assertIn(base+'emergency-contact/',self.browser.current_url)

        #fills out emergency contact form
        self.fill_out_emergency_contact()
        #proceeds to address form
        self.assertIn(base+'address/',self.browser.current_url)

        #fills out address form
        self.fill_out_address_form()
        #proceeds to LG form
        self.assertIn(base+'lifeguard-information/',self.browser.current_url)

        #fills out LG form
        self.fill_out_lifeguard_form()
        #is taken to a Lifguard Classes page which lists the available classes
        self.assertIn('lifeguard/classes',self.browser.current_url)

        #picks a class to attend
        enrollment_btns = self.browser.find_elements_by_name('enroll-btn')
        enrollment_btns[0].submit()
        self.assertEqual(Enroll.objects.count(),1)

        #makes payment

        #redirect to dashboard

    def sign_up(self):
        #signs up
        email_input = self.browser.find_element_by_id('id_email')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')

        test_email = 'test@example.com'
        test_password = 'u7efd!hd'
        email_input.send_keys(test_email)
        password1_input.send_keys(test_password)
        password2_input.send_keys(test_password)

        #submit form
        self.browser.find_element_by_id('signup-form').submit()

    def fill_out_contact_information(self):
        first_name = "John"
        last_name = "Doe"
        phone = "713 434 4564"
        dob = "2000-06-09"
        self.browser.find_element_by_id('id_first_name').send_keys(first_name)
        self.browser.find_element_by_id('id_last_name').send_keys(last_name)
        self.browser.find_element_by_id('id_phone').send_keys(phone)
        self.browser.find_element_by_id('id_dob').send_keys(dob)
        self.browser.find_element_by_id('contact_information_form').submit()

    def fill_out_emergency_contact(self):
        emergency_contact = "Mary Jane"
        relationship = "Mom"
        phone = "834 283 2838"
        self.browser.find_element_by_id('id_name').send_keys(emergency_contact)
        self.browser.find_element_by_id('id_relationship').send_keys(relationship)
        self.browser.find_element_by_id('id_phone').send_keys(relationship)
        self.browser.find_element_by_id('emergency_contact_form').submit()

    def fill_out_address_form(self):
        street1 = "123 Main St"
        city = "San Diego"
        state = "CA"
        zip_code = "94103"
        self.browser.find_element_by_id('id_street1').send_keys(street1)
        self.browser.find_element_by_id('id_city').send_keys(city)
        self.browser.find_element_by_id('id_state').send_keys(state)
        self.browser.find_element_by_id('id_zip').send_keys(zip_code)
        self.browser.find_element_by_id('address_form').submit()

    def fill_out_lifeguard_form(self):
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

class LogInTest(BaseTestFixture):

    def setUp(self):
        super().setUp()
        self.credentials = {'username':'test@example.com', 'password':'u7efd!hd'}
        User.objects.create_user(email=self.credentials['username'],password=self.credentials['password'])

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

    def test_at_password_reset_page(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/password_reset/'))
        self.assertIn('Password Reset',self.browser.title)

    def test_can_reset_password(self):
        #user already has an account
        email = 'test@example.com'
        password = 'u7efd!hd'
        user = User.objects.create_user(email=email,password=password)

        #user forgot their password
        self.browser.get('%s%s' % (self.live_server_url,'/users/password_reset/'))
        self.browser.find_element_by_id('id_email').send_keys(user.email)
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
        self.browser.find_element_by_id('id_username').send_keys(user.email)
        self.browser.find_element_by_id('id_password').send_keys(new_password)
        self.browser.find_element_by_id('login-form').submit()
        self.assertIn('dashboard',self.browser.current_url)


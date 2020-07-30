import time
import unittest
import re

from django.test import LiveServerTestCase
from django.core import mail
from django.urls import reverse,reverse_lazy

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from users.models import User

class BaseTestFixture(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

class SignUpTest(BaseTestFixture):

    def test_at_signup_page(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/signup'))
        self.assertIn('Sign-Up',self.browser.title)


    def test_sign_up(self):
        #user lands on homepage
        self.browser.get('%s%s' % (self.live_server_url,'/home'))
        self.assertIn('Home',self.browser.title)

        #wants to sign up
        self.browser.find_element_by_id('id_signup').click()
        self.assertIn('signup',self.browser.current_url)

        #signs up
        email_input = self.browser.find_element_by_id('id_email')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')
        email_input.send_keys('test@example.com')
        test_password = 'u7efd!hd'
        password1_input.send_keys(test_password)
        password2_input.send_keys(test_password)
        self.browser.find_element_by_id('signup-form').submit()

        #redirected to dashboard on successful sign up
        self.assertIn('dashboard',self.browser.current_url)

class LifeguardRegistrationTest(BaseTestFixture):

    def setUp(self):
        super().setUp()
        #user already has an account
        self.user = User.objects.create(email="test@example.com", password="u7hfdj4")

    def test_new_lifeguard_registration(self):

        #start at dashboard
        self.browser.get('%s%s' % (self.live_server_url,'/users/dashboard'))

        #clicks on LG registration form
        self.browser.find_element_by_id('id_lifeguard_registration').click()
        self.assertIn('lifeguard-registration',self.browser.current_url)

        #fills out contact information form

        #fills out emergency contact form

        #is asked if they are already certified

        #user is a new lifeguard

        #fills out LG form

        #picks a class to attend

        #makes payment

        #redirect to dashboard





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


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
        self.browser.get('%s%s' % (self.live_server_url,'/users/signup'))
        email_input = self.browser.find_element_by_id('id_email')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')
        email_input.send_keys('test@example.com')
        test_password = 'u7efd!hd'
        password1_input.send_keys(test_password)
        password2_input.send_keys(test_password)
        self.browser.find_element_by_id('signup-form').submit()
        #check user is redirected to dashboard on successful sign up
        self.assertIn('dashboard',self.browser.current_url)

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
        email = 'test@example.com'
        password = 'u7efd!hd'
        user = User.objects.create_user(email=email,password=password)

        self.browser.get('%s%s' % (self.live_server_url,'/users/password_reset/'))
        self.browser.find_element_by_id('id_email').send_keys(user.email)
        self.browser.find_element_by_id('forgot-password-form').submit()

        self.assertEqual(len(mail.outbox),1)
        self.assertIn('reset',mail.outbox[0].subject)

        match = re.search(r'http:\/\/[\w]+:[\w]+\/users\/password_reset_confirm\/[\w]+\/.+\/',mail.outbox[0].body)
        self.assertTrue(match)

        reset_url = match[0]
        self.browser.get(reset_url)
        self.assertIn('Change password',self.browser.page_source)
        time.sleep(10)




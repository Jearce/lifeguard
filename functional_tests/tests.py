from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

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

class LogInTest(BaseTestFixture):

    def setUp(self):
        super().setUp()
        self.credentials = {'username':'test@example.com', 'password':'u7efd!hd'}

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

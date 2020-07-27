from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

class SignUpTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

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

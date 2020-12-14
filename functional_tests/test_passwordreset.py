import re
import os

from django.core import mail

from users.models import User

from functional_tests.helpers import BaseTestFixture
from utils.test.helpers import create_user

DOMAIN = "http:\/\/example.com\/"

class PasswordResetTest(BaseTestFixture):
    def setUp(self):
        super().setUp()
        #user already has an account
        self.user = create_user()[0]

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

        pattern = r'http:\/\/example.com\/users\/password_reset_confirm\/[\w]+\/.+\/'

        #r'http:\/\/[\w]+:[\w]+\/users\/password_reset_confirm\/[\w]+\/.+\/',
        match = re.search(pattern,mail.outbox[0].body)
        self.assertTrue(match)

        passwordreset_url = match[0]
        url = self.live_server_url + passwordreset_url[18:]

        self.browser.get(url)
        self.assertIn('Change password',self.browser.page_source)

        #user resets password
        new_password = 'newPasswordTest123!'
        self.browser.find_element_by_id('id_new_password1').send_keys(new_password)
        self.browser.find_element_by_id('id_new_password2').send_keys(new_password)
        self.browser.find_element_by_id('change-password-form').submit()
        self.assertIn('complete',self.browser.current_url)

        #user gets redirected to login page after resetting password
        self.browser.find_element_by_id('id_login_from_password_reset').click()
        self.assertIn('login',self.browser.current_url)

        #user logs in with new password
        self.browser.find_element_by_id('id_username').send_keys(self.user.email)
        self.browser.find_element_by_id('id_password').send_keys(new_password)
        self.browser.find_element_by_id('login-form').submit()
        self.assertIn('dashboard',self.browser.current_url)

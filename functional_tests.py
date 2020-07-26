from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

class SignUpTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_sign_up(self):
        self.browser.get('http://127.0.0.1:7000/users/signup/')
        self.assertIn('Sign-Up',self.browser.title)

        test_email = 'test@example.com'
        test_password = 'sdfne134d'

        email = self.browser.find_element_by_id('id_email')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')

        email.send_keys(test_email)
        password1.send_keys(test_password)
        password2.send_keys('not the same')
        self.browser.find_element_by_id('signup-form').submit()
        time.sleep(10)

if __name__ == '__main__':
    unittest.main()

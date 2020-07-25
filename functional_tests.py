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
        self.browser.get('http://localhost:700/signup/')
        self.assertIn('Sign-Up',self.browser.title)

if __name__ == '__main__':
    unittest.main()

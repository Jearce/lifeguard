import time

from django.conf import settings

from employee.models import Employee, Transportation, Position

from functional_tests.helpers import BaseTestLoginFixture
from functional_tests import helpers
from utils.test.helpers import create_user

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_DIR = settings.BASE_DIR


class AdminTest(BaseTestLoginFixture):
    def setUp(self):
        super().setUp()
        self.user.is_superuser = True
        self.user.save()

    def test_is_super_user(self):
        self.assertTrue(self.user.is_superuser)

    def test_has_access_to_admin_panel(self):
        self.login()
        self.browser.find_element_by_id("id_admin_panel").click()
        self.assertIn("admin-panel", self.browser.current_url)

    def test_can_add_user(self):
        self.login()
        self.browser.find_element_by_id("id_admin_panel").click()
        self.browser.find_element_by_id("id_add_user").click()
        self.assertIn("add-user",self.browser.current_url)
        credentials = {
            'email':'another@example.com',
            'first_name':'Larry',
            'last_name':'John',
            'phone':'121 382 8292',
            'dob':'09/06/1995',
            'street1':"123 Main St",
            'state':'Oregon',
            'city':'Portland',
            'zip':'97035',
            'password1':'2dhd7!42',
            'password2':'2dhd7!42'
        }
        self.general_form_input(credentials,form_id="signup_form")
        self.assertIn('admin-panel',self.browser.current_url)


 
        

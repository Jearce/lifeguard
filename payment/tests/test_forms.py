from django.test import TestCase

from utils.test import helpers

class LifeguardCheckoutFormTest(TestCase):

    def setUp(self):
        super().setUp()
        self.user,self.email,self.password,self.credentials = helpers.create_user()

    def test_initial_billing_address_is_set(self):



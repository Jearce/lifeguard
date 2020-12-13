from functional_tests.helpers import BaseTestFixture

class SignUpTest(BaseTestFixture):
    def setUp(self):
        #user lands on homepage
        self.browser.get(self.live_server_url)

    def test_signup(self):
        self.signup()
        self.fill_out_emergency_contact()

    def signup(self):
        credentials = {
            'email':'test@example.com',
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

        #select account opitions to get to sign up link
        self.browser.find_element_by_class_name('navbar-toggler').click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_id('navbarDropdown').click()
        self.browser.find_element_by_id('id_signup').click()

        self.assertIn('signup',self.browser.current_url)
        self.general_form_input(credentials,form_id="signup_form")
        self.assertIn('emergency-contact/',self.browser.current_url)

from functional_tests.helpers import BaseTestFixture

class SignUpTest(BaseTestFixture):
    def setUp(self):
        #user lands on homepage
        self.start_at_home_page()

    def test_signup(self):
        self.signup()
        self.fill_out_emergency_contact()

    def signup(self):
        #select account opitions to get to sign up link
        self.browser.find_element_by_class_name('navbar-toggler').click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_id('navbarDropdown').click()
        self.browser.find_element_by_id('id_signup').click()

        self.assertIn('signup',self.browser.current_url)
        self.general_form_input(self.credentials,form_id="signup_form")
        self.assertIn('emergency-contact/',self.browser.current_url)

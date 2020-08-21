import re
import time

from django.core import mail
from django.urls import reverse,reverse_lazy

from selenium.webdriver.common.keys import Keys

from users.models import User,EmergencyContact,Address
from lifeguard.models import LifeguardClass,Enroll,Lifeguard
from employee.models import Transportation,Position

from .helpers import BaseTestFixture

class SignUpTest(BaseTestFixture):
    def setUp(self):
        #user lands on homepage
        self.start_at_home_page()

    def test_register_as_new_lifeguard_and_employee(self):

        #creates account and is taken to the dashboard
        self.sign_up()
        #clicks on lifeguard registration link
        self.start_registration(element_id='id_lifeguard_registration')

        #fills out contact information,emergency contact,and address forms
        self.fill_out_contact_information()
        self.fill_out_emergency_contact()
        self.fill_out_address_form(redirect_url='/lifeguard/create/')

        #fills out lifeguard form and selects they want to work for company
        self.register_new_lifeguard_who_wants_to_work(redirect_url="/employee/create/")

        #now fills out employee,education, and job history forms
        self.fill_employee_form({**self.employee_data,**self.lifeguard_and_supervisor})
        self.fill_employee_education_form()
        self.fill_employee_job_history(redirect_url="lifeguard/classes/")

        #picks a class to attend
        self.enroll_in_class()

        #makes payment
        self.fail("Finish Payment Test")

        #redirect to dashboard

    def test_register_as_employee_and_apply_as_nonlifeguard(self):
        #creates account and is taken to the dashboard
        self.sign_up()

        #clicks on employee registration link
        self.start_registration(element_id='id_employee_registration')

        #fills out contact information,emergency contact,and address forms
        self.fill_out_contact_information()
        self.fill_out_emergency_contact()
        self.fill_out_address_form(redirect_url="employee/create/")

        #now fills out employee,education, and job history forms
        self.fill_employee_form({**self.employee_data,**self.only_supervisor})
        self.fill_employee_education_form()
        self.fill_employee_job_history(redirect_url="/users/dashboard/")

        self.fail("Wait for application status")

    def test_register_as_employee_and_apply_as_lifeguard(self):
        #creates account and is taken to the dashboard
        self.sign_up()

        #clicks on employee registration link
        self.start_registration(element_id='id_employee_registration')

        #fills out contact information,emergency contact,and address forms
        self.fill_out_contact_information()
        self.fill_out_emergency_contact()
        self.fill_out_address_form(redirect_url="employee/create/")

        #now fills out employee,education, and job history forms
        self.fill_employee_form({**self.employee_data,**self.lifeguard_and_supervisor})
        self.fill_employee_education_form()
        self.fill_employee_job_history(redirect_url="/lifeguard/create/")

        #register lifeguard who is already filled out the employee application
        self.register_new_lifeguard_who_applied_as_employee(redirect_url="/lifeguard/classes/")

        #picks a class to attend
        self.enroll_in_class()

        #makes payment
        self.fail("Finish Payment Test")

    def test_register_as_certified_lifeguard(self):

        #creates account and is taken to the dashboard
        self.sign_up()

        #clicks on lifeguard registration link
        self.start_registration(element_id='id_lifeguard_registration')

        #fills out contact information,emergency contact,and address forms
        self.fill_out_contact_information()
        self.fill_out_emergency_contact()
        self.fill_out_address_form(redirect_url='/lifeguard/create/')

        #register lifeguard who is already filled out the employee application
        self.register_returning_lifeguard_who_applied_as_employee(redirect_url="/lifeguard/already-certified/")
        self.fill_already_lifeguard_form(redirect_url="/employee/create/")

        #now fills out employee,education, and job history forms
        self.fill_employee_form({**self.employee_data,**self.lifeguard_and_supervisor})
        self.fill_employee_education_form()
        self.fill_employee_job_history(redirect_url="/lifeguard/classes/")

        #picks a class to attend
        self.enroll_in_class()

        #makes payment
        self.fail("Finish Payment Test")




    def sign_up(self):
        #select account opitions to get to sign up link
        self.browser.find_element_by_class_name('navbar-toggler').click()
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_id('navbarDropdown').click()
        self.browser.find_element_by_id('id_signup').click()
        self.assertIn('signup',self.browser.current_url)

        email_input = self.browser.find_element_by_id('id_email')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')

        email = self.credentials['username']
        password = self.credentials['password']

        email_input.send_keys(email)
        password1_input.send_keys(password)
        password2_input.send_keys(password)

        self.browser.find_element_by_id('signup-form').submit()
        self.assertIn('dashboard',self.browser.current_url)

class LogInTest(BaseTestFixture):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            email=self.credentials['username'],
            password=self.credentials['password']
        )
        EmergencyContact.objects.create(user=self.user,**self.emergency_contact)
        Address.objects.create(user=self.user,**self.address)

    def test_at_login_page(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        self.assertIn('Login',self.browser.title)

    def test_login(self):
        self.login()

    def test_login_and_finish_lifeguard_and_employee_application(self):
        self.login()
        self.start_registration(element_id='id_lifeguard_registration')

        #already filled out contact information,emergency contact, and address forms
        self.submit_form(form_id="contact_information_form")
        self.submit_form(form_id="emergency_contact_form")
        self.submit_form(form_id="address_form")

        #finish lifeguard form
        self.register_new_lifeguard_who_wants_to_work(redirect_url="/employee/create/")

        #and employee forms
        self.fill_employee_form({**self.employee_data,**self.lifeguard_and_supervisor})
        self.fill_employee_education_form()
        self.fill_employee_job_history(redirect_url="lifeguard/classes/")

        self.enroll_in_class()

        self.fail("Finish payment test")


    def login(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        self.general_form_input(self.credentials,'login-form')
        #check user is redirected to dashboard on successful login
        self.assertIn('dashboard',self.browser.current_url)

    def submit_form(self,form_id):
        self.browser.find_element_by_id(form_id).submit()

class PasswordResetTest(BaseTestFixture):

    def setUp(self):
        super().setUp()
        #user already has an account
        self.user = User.objects.create_user(
            email=self.credentials['username'],
            password=self.credentials['password']
        )

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
        match = re.search(r'http:\/\/[\w]+:[\w]+\/users\/password_reset_confirm\/[\w]+\/.+\/',mail.outbox[0].body)
        self.assertTrue(match)
        reset_url = match[0]
        self.browser.get(reset_url)
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

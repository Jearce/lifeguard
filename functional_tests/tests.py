import time
import unittest
import re

from django.test import LiveServerTestCase
from django.core import mail
from django.urls import reverse,reverse_lazy

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from users.models import User
from lifeguard.models import LifeguardClass,Enroll
from employee.models import Transportation,Position

class BaseTestFixture(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        cls.credentials = {
            'username':'test@example.com',
            'password':'u7efd!hd',
        }
        cls.contact_information = {
            'first_name':'John',
            'last_name' : 'Doe',
            'phone' : '713 434 4564',
            'dob' : '2000-06-09'
        }

        cls.address = {
           'street1' : "123 Main St",
           'city' : "San Diego",
           'state' : "CA",
           'zip' : "94103"
        }
        cls.emergency_contact = {
            'name':'Mary Jane',
            'relationship':'Mom',
            'phone':'832 283 2834',
        }
        cls.employee_data = {
            "home_phone":"712 634 3328",
            "who_referred_you":"A friend.",
            "transportation":"Car",
            "applied_positions_1":"click",
            "applied_positions_2":"click",
            "start_date":"8/8/2020",
            "end_date":"12/8/2021",
            "work_hours_desired":"40",
            "desired_pay_rate":"17.50",
            "pool_preference":"Village Pool",
            "subdivision":"My subdivision 122",
            "work_authorization_1":"click",
            "charged_or_arrested_2":"click",
            "has_felony_2":"click",
            "contract_employment_agreement":"click",
            "electronic_signature":"Larry Johnson",
        }
        cls.employee_education = {
            "school_name":"Django College",
            "grade_year":"Freshmen",
            "attending_college":"click",
            "date_leaving_to_college":"9/10/2020"
        }
        cls.employee_job_history = {
            "previous_employer":"Some Company",
            "job_title":"Tester",
            "salary":"18.65",
            "start_date":"2010-06-09",
            "end_date":"2020-06-09",
            "reason_for_leaving":"I've done all I can there.",
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.quit()

    def enroll_in_class(self):
        enrollment_btns = self.browser.find_elements_by_name('enroll-btn')

        #choose an avaliable class
        enrollment_btns[0].submit()
        self.assertEqual(Enroll.objects.count(),1)
        self.assertIn('users/dashboard/',self.browser.current_url)

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

    def fill_out_contact_information(self):
        self.general_form_input(self.contact_information,form_id="contact_information_form")
        self.assertIn('emergency-contact/',self.browser.current_url)

    def fill_out_address_form(self,redirect_url):
        self.general_form_input(self.address,form_id="address_form")
        self.assertIn(redirect_url,self.browser.current_url)

    def fill_employee_form(self):
        self.general_form_input(self.employee_data,form_id="employee_form")
        self.assertIn('employee/education/',self.browser.current_url)

    def register_new_lifeguard_who_wants_to_work(self):
        #user is a new lifeguard
        register_data = {
           "already_certified" : "N", #user is a new lifeguard
           "wants_to_work_for_company":"Y", #and wants to work as a lifeguard
           "payment_agreement":"click",
           "payment_agreement_signature":"Larry Jones",
           "no_refunds_agreement" : "click",
           "electronic_signature" : "Larry Jones"
        }
        self.general_form_input(register_data,form_id="lifeguard_form")
        self.assertIn('employee/create/',self.browser.current_url)

    def fill_out_emergency_contact(self):
        prefix = 'id_emergencycontact_set'
        self.general_managment_form_input(
            records=[self.emergency_contact],
            form_id="emergency_contact_form",
            prefix=prefix
        )
        self.assertIn('address/',self.browser.current_url)

    def fill_employee_education_form(self):
        prefix = 'id_employeeeducation_set'
        self.general_managment_form_input(
            records=[self.employee_education],
            form_id="education_form",
            prefix=prefix
        )
        self.assertIn('employee/job-history/',self.browser.current_url)

    def fill_employee_job_history(self):
        prefix = 'id_jobhistory_set'
        self.general_managment_form_input(
            records=[self.employee_job_history],
            form_id="job_history_form",
            prefix=prefix
        )
        self.assertIn('lifeguard/classes/',self.browser.current_url)

    def start_at_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Home',self.browser.title)

    def start_registration(self,element_id):
        self.browser.find_element_by_id(element_id).click()
        self.assertIn('contact-information/',self.browser.current_url)

    def from_dashboard_click(self,element_id):
        self.browser.find_element_by_id(element_id).click()

    def general_form_input(self,data,form_id):
        for key,value in data.items():
            element = self.browser.find_element_by_id(f"id_{key}")
            if value == 'click':
                element.click()
            else:
                element.send_keys(value)
        self.browser.find_element_by_id(form_id).submit()

    def general_managment_form_input(self,records,form_id,prefix):
        for i,record in enumerate(records):
            for key,value in record.items():
                element = self.browser.find_element_by_id(f"{prefix}-{i}-{key}")
                if value == 'click':
                    element.click()
                else:
                    element.send_keys(value)
        self.browser.find_element_by_id(form_id).submit()

    def enroll_in_class(self):
        enrollment_btns = self.browser.find_elements_by_name('enroll-btn')

        #choose an avaliable class
        enrollment_btns[0].submit()
        self.assertEqual(Enroll.objects.count(),1)
        self.assertIn('users/dashboard/',self.browser.current_url)

    def make_payment(self):
        pass


class SignUpTest(BaseTestFixture):

    def setUp(self):
        Position.objects.create(title="Lifeguard",age_requirement="Must be 15 years or older")
        Position.objects.create(title="Supervisor",age_requirement="Must be 18 years or older")
        Transportation.objects.create(name="Car",description="I will drive my self.")

        class1 = {
            "course":"Review",
            "start_date":"2020-8-28 14:30:59",
            "end_date":"2020-9-8 14:30:59",
            "cost":120.23,
            "employee_cost":50.50
        }
        class2 = {
            "course":"Lifeguard",
            "start_date":"2020-8-28 14:30:59",
            "end_date":"2020-9-8 14:30:59",
            "cost":120.23,
            "employee_cost":50.50
        }
        LifeguardClass.objects.bulk_create(
            [LifeguardClass(**class1),
             LifeguardClass(**class2)]
        )

    def test_sign_up_and_register_as_new_lifeguard_and_employee(self):
        #user lands on homepage
        self.start_at_home_page()
        #creates account and is taken to the dashboard
        self.sign_up()
        #clicks on lifeguard registration link
        self.start_registration(element_id='id_lifeguard_registration')

        #fills out contact information,emergency contact,and address forms
        self.fill_out_contact_information()
        self.fill_out_emergency_contact()
        self.fill_out_address_form(redirect_url='/lifeguard/create/')

        #fills out lifeguard form and selects they want to work for company
        self.register_new_lifeguard_who_wants_to_work()

        #now fills out employee,education, and job history forms
        self.fill_employee_form()
        self.fill_employee_education_form()
        self.fill_employee_job_history()

        #picks a class to attend
        self.enroll_in_class()

        #makes payment
        self.fail("Finish payment")

        #redirect to dashboard

    def test_sign_up_and_register_as_employee(self):
        #user lands on homepage
        self.start_at_home_page()

        #creates account and is taken to the dashboard
        self.sign_up()

        #clicks on employee registration link
        self.start_registration(element_id='id_employee_registration')

        #fills out contact information,emergency contact,and address forms
        self.fill_out_contact_information()
        self.fill_out_emergency_contact()
        self.fill_out_address_form(redirect_url="employee/create/")

class LogInTest(BaseTestFixture):

    def setUp(self):
        super().setUp()
        User.objects.create_user(
            email=self.credentials['username'],
            password=self.credentials['password']
        )

    def test_at_login_page(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        self.assertIn('Login',self.browser.title)

    def test_login(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        self.general_form_input(self.credentials,'login-form')
        #check user is redirected to dashboard on successful login
        self.assertIn('dashboard',self.browser.current_url)

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
        self.browser.find_element_by_id('id_login').click()
        self.assertIn('login',self.browser.current_url)

        #user logs in with new password
        self.browser.find_element_by_id('id_username').send_keys(self.user.email)
        self.browser.find_element_by_id('id_password').send_keys(new_password)
        self.browser.find_element_by_id('login-form').submit()
        self.assertIn('dashboard',self.browser.current_url)

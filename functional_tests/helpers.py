import time
import os

from django.test import LiveServerTestCase
from django.contrib.sites.models import Site
from django.conf import settings

from selenium import webdriver
import selenium

from users.models import User,EmergencyContact,Address
from lifeguard.models import LifeguardClass,Enroll,Lifeguard
from employee.models import Transportation,Position,Employee,PDFFile

from utils.test.helpers import create_user

BASE_DIR = settings.BASE_DIR

class BaseTestFixture(LiveServerTestCase):
    fixtures = ['classes.json','positions.json','transportation.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

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
            "start_date":"8/8/2020",
            "end_date":"12/8/2021",
            "work_hours_desired":"40",
            "desired_pay_rate":"17.50",
            "pool_preference":"Village Pool",
            "subdivision":"My subdivision 122",
            "work_authorization_1":"click",
            "charged_or_arrested_resolved_2":"click",
            "charged_or_arrested_not_resolved_2":"click",
            "contract_employment_agreement":"click",
            "electronic_signature":"Larry Johnson",
        }

        cls.lifeguard_and_supervisor = {
            "applied_positions_1":"click",
            "applied_positions_2":"click",
        }

        cls.only_supervisor = {
            "applied_positions_2":"click",
        }

        cls.employee_job_history = {
            "previous_employer":"Some Company",
            "job_title":"Tester",
            "salary":"18.65",
            "start_date":"09/05/2019",
            "end_date":"04/06/2020",
            "reason_for_leaving":"I've done all I can there.",
        }

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def fill_out_contact_information(self):
        self.general_form_input(self.contact_information,form_id="contact_information_form")
        self.assertIn('emergency-contact/',self.browser.current_url)

    def fill_out_address_form(self,redirect_url):
        self.general_form_input(self.address,form_id="address_form")
        self.assertIn(redirect_url,self.browser.current_url)
        self.general_form_input(data,form_id="employee_form")
        self.assertIn('employee/education/',self.browser.current_url)

    def fill_out_emergency_contact(self):
        prefix = 'id_emergencycontact_set'
        self.general_managment_form_input(
            records=[self.emergency_contact],
            form_id="emergency_contact_form",
            prefix=prefix
        )
        self.assertIn('/users/dashboard/',self.browser.current_url)

    def general_form_input(self,data,form_id,submit=True):
        for key,value in data.items():
            try:
                element = self.browser.find_element_by_id(f"id_{key}")
            except selenium.common.exceptions.NoSuchElementException:
                element = self.browser.find_element_by_xpath(f"//input[@name='{key}']")

            if value == 'click':
                try:
                    element.click()
                except selenium.common.exceptions.ElementClickInterceptedException:
                    self.browser.execute_script("arguments[0].click();",element)
            else:
                element.send_keys(value)

        if submit: self.browser.find_element_by_id(form_id).submit()

    def general_managment_form_input(self,records,form_id,prefix):
        for i,record in enumerate(records):
            for key,value in record.items():
                element = self.browser.find_element_by_id(f"{prefix}-{i}-{key}")
                if value == 'click':
                    element.click()
                else:
                    element.send_keys(value)
        self.browser.find_element_by_id(form_id).submit()

class BaseTestLoginFixture(BaseTestFixture):
    def setUp(self):
        super().setUp()
        user_and_data = create_user()
        self.user = user_and_data[0]
        self.email = user_and_data[1]
        self.password = user_and_data[2]

        self.path_to_files = os.path.join(BASE_DIR,"functional_tests/files_used_to_test")
        PDFFile.objects.create(
            site=Site.objects.get_current(),
            w4=f"{self.path_to_files}/w4.pdf",
            i9=f"{self.path_to_files}/i9.pdf",
            workers_comp=f"{self.path_to_files}/workers_comp.pdf",
        )

        EmergencyContact.objects.create(user=self.user,**self.emergency_contact)
        Address.objects.create(user=self.user,**self.address)

    def login(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        self.general_form_input(
            {'username':self.email,'password':self.password}
            ,form_id='login-form')
        #check user is redirected to dashboard on successful login
        self.assertIn('dashboard',self.browser.current_url)

    def fill_employee_form(self,data):
        self.general_form_input(data,form_id="employee_form")
        self.assertIn('employee/education/',self.browser.current_url)

    def fill_employee_education_form(self):
        employee_education = {
            "school_name":"Django College",
            "grade_year":"Freshmen",
            "attending_college":"Yes",
            "date_leaving_to_college":"9/10/2020"
        }
        prefix = 'id_employeeeducation_set'
        self.general_managment_form_input(
            records=[employee_education],
            form_id="education_form",
            prefix=prefix
        )
        self.assertIn('employee/job-history/',self.browser.current_url)

    def fill_employee_job_history(self,redirect_url):
        prefix = 'id_jobhistory_set'
        self.general_managment_form_input(
            records=[self.employee_job_history],
            form_id="job_history_form",
            prefix=prefix
        )
        self.assertIn(redirect_url,self.browser.current_url)

    def enroll_in_class(self):
        enrollment_btns = self.browser.find_elements_by_name('enroll-btn')

        #choose an avaliable class
        enrollment_btns[0].submit()
        self.assertEqual(Enroll.objects.count(),1)
        self.assertIn('payment/enrollment-cart/',self.browser.current_url)


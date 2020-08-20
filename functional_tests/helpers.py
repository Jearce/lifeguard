import time
import os

from django.test import LiveServerTestCase

from selenium import webdriver

from lifeguard.models import Enroll


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BaseTestFixture(LiveServerTestCase):
    fixtures = ['classes.json','positions.json','transportation.json']

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

        cls.lifeguard_and_supervisor = {
            "applied_positions_1":"click",
            "applied_positions_2":"click",
        }

        cls.only_supervisor = {
            "applied_positions_2":"click",
        }

        cls.employee_education = {
            "school_name":"Django College",
            "grade_year":"Freshmen",
            "attending_college":"Yes",
            "date_leaving_to_college":"9/10/2020"
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

    def enroll_in_class(self):
        enrollment_btns = self.browser.find_elements_by_name('enroll-btn')

        #choose an avaliable class
        enrollment_btns[0].submit()
        self.assertEqual(Enroll.objects.count(),1)
        self.assertIn('users/dashboard/',self.browser.current_url)

    def fill_out_contact_information(self):
        self.general_form_input(self.contact_information,form_id="contact_information_form")
        self.assertIn('emergency-contact/',self.browser.current_url)

    def fill_out_address_form(self,redirect_url):
        self.general_form_input(self.address,form_id="address_form")
        self.assertIn(redirect_url,self.browser.current_url)

    def fill_employee_form(self,data):
        self.general_form_input(data,form_id="employee_form")
        self.assertIn('employee/education/',self.browser.current_url)

    def fill_returning_lifeguard_form(self,redirect_url):
        register_data = {
           "already_certified" : "Y",
           "payment_agreement":"click",
           "payment_agreement_signature":"Larry Jones",
           "no_refunds_agreement" : "click",
           "electronic_signature" : "Larry Jones"
        }
        self.general_form_input(register_data,form_id="lifeguard_form")
        self.assertIn(redirect_url,self.browser.current_url)

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

    def fill_employee_job_history(self,redirect_url):
        prefix = 'id_jobhistory_set'
        self.general_managment_form_input(
            records=[self.employee_job_history],
            form_id="job_history_form",
            prefix=prefix
        )
        self.assertIn(redirect_url,self.browser.current_url)

    def fill_already_lifeguard_form(self,redirect_url):
        data = {
            "last_certified":'05/11/2020',
            "certification":os.path.join(BASE_DIR,'lifeguard/tests/certificate.pdf'),
        }
        self.general_form_input(data,form_id="already_certified_form")
        self.assertIn(redirect_url,self.browser.current_url)

    def register_new_lifeguard_who_wants_to_work(self,redirect_url):
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
        self.assertIn(redirect_url,self.browser.current_url)

    def register_new_lifeguard_who_applied_as_employee(self,redirect_url):
        register_data = {
           "already_certified" : "N",
           "payment_agreement":"click",
           "payment_agreement_signature":"Larry Jones",
           "no_refunds_agreement" : "click",
           "electronic_signature" : "Larry Jones"
        }
        self.general_form_input(register_data,form_id="lifeguard_form")
        self.assertIn(redirect_url,self.browser.current_url)

    def register_returning_lifeguard_who_applied_as_employee(self,redirect_url):
        register_data = {
           "already_certified" : "Yes",
           "wants_to_work_for_company":"Yes", #and wants to work as a lifeguard
           "payment_agreement":"click",
           "payment_agreement_signature":"Larry Jones",
           "no_refunds_agreement" : "click",
           "electronic_signature" : "Larry Jones"
        }
        self.general_form_input(register_data,form_id="lifeguard_form")
        self.assertIn(redirect_url,self.browser.current_url)

    def start_at_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Home',self.browser.title)

    def start_registration(self,element_id):
        self.browser.find_element_by_id(element_id).click()
        self.assertIn('contact-information/',self.browser.current_url)

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



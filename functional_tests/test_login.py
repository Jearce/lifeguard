import os

from django.conf import settings
from django.contrib.sites.models import Site


from users.models import User,EmergencyContact,Address
from lifeguard.models import LifeguardClass,Enroll,Lifeguard
from employee.models import Transportation,Position,Employee,PDFFile

from functional_tests.helpers import BaseTestFixture
from functional_tests import helpers

BASE_DIR = settings.BASE_DIR

class LoginTest(BaseTestFixture):
    def setUp(self):
        super().setUp()
        self.user = self.create_user()

        EmergencyContact.objects.create(user=self.user,**self.emergency_contact)
        Address.objects.create(user=self.user,**self.address)

        path_to_files = os.path.join(BASE_DIR,"functional_tests/files_used_to_test")
        PDFFile.objects.create(
            site=Site.objects.get_current(),
            w4=f"{path_to_files}/w4.pdf",
            i9=f"{path_to_files}/i9.pdf",
            workers_comp=f"{path_to_files}/workers_comp.pdf",
        )

        self.employee_checklist = {
            "photo_id":f"{path_to_files}/photoid.pdf",
            "social_security_card":f"{path_to_files}/social.pdf",
            "social_security_number":"444-44-444",
            "birth_certificate":f"{path_to_files}/birthcertificate.pdf",
            "w4":f"{path_to_files}/w4.pdf",
            "i9":f"{path_to_files}/i9.pdf",
            "workers_comp":f"{path_to_files}/workers_comp.pdf",
            "vaccination_record":f"{path_to_files}/vaccination.pdf",
            "banking_name":"Banking 123",
            "account_type_1":"click",#choose savings
            "account_number":"19282739",
            "savings_number":"1728327",
            "email_address":self.user.email,
            "auth_signature":"Larry Johnson",
            "awknowledgement_form_signature":"Larry Johnson",
        }

    def test_at_login_page(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        self.assertIn('Login',self.browser.title)

    def test_login(self):
        self.login()

    def test_register_new_lifeguard_and_employee(self):

        self.login()

        #clicks on lifeguard registration link
        self.browser.find_element_by_id('id_lifeguard_registration').click()

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

    def test_register_as_certified_lifeguard_and_employee(self):
        self.login()

        #clicks on lifeguard registration link
        self.browser.find_element_by_id('id_lifeguard_registration').click()

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

    def test_register_as_employee_and_apply_as_nonlifeguard(self):
        self.login()

        #clicks on employee registration link
        self.browser.find_element_by_id('id_employee_registration').click()

        #now fills out employee,education, and job history forms
        #only applies to a non lifeguard position
        self.fill_employee_form({**self.employee_data,**self.only_supervisor})
        self.fill_employee_education_form()
        self.fill_employee_job_history(redirect_url="/users/dashboard/")

        self.fail("Wait for application status")

    def test_register_as_employee_and_apply_as_lifeguard(self):
        #creates account and is taken to the dashboard
        self.login()

        #clicks on employee registration link
        self.browser.find_element_by_id('id_employee_registration').click()

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

    def test_check_application_status(self):
        employee = Employee.objects.create(
            user=self.user,
            home_phone="712 634 3328",
            who_referred_you="A friend.",
            transportation=Transportation.objects.all()[0],
            start_date="2020-8-8",
            end_date="2021-12-8",
            work_hours_desired="40",
            desired_pay_rate="17.50",
            pool_preference="Village Pool",
            subdivision="My subdivision 122",
            work_authorization=True,
            charged_or_arrested_resolved=False,
            charged_or_arrested_not_resolved=False,
            contract_employment_agreement=True,
            electronic_signature="Larry Johnson",
        )
        employee.applied_positions.set(Position.objects.all())
        employee.save()

        self.login()
        self.browser.find_element_by_id('application_status').click()
        self.assertIn('/application-status/',self.browser.current_url)

    def test_complete_employee_checklist(self):
        employee = Employee.objects.create(
            user=self.user,
            home_phone="712 634 3328",
            who_referred_you="A friend.",
            transportation=Transportation.objects.all()[0],
            start_date="2020-8-8",
            end_date="2021-12-8",
            work_hours_desired="40",
            desired_pay_rate="17.50",
            pool_preference="Village Pool",
            subdivision="My subdivision 122",
            work_authorization=True,
            charged_or_arrested_resolved=False,
            charged_or_arrested_not_resolved=False,
            contract_employment_agreement=True,
            electronic_signature="Larry Johnson",
        )
        employee.applied_positions.set(Position.objects.all())
        employee.is_hired = True
        employee.save()

        self.login()
        self.browser.find_element_by_id('employee_checklist').click()
        self.assertIn('/employee-checklist/',self.browser.current_url)
        self.fill_employee_checklist(redirect_url="/users/dashboard/")

    def login(self):
        self.browser.get('%s%s' % (self.live_server_url,'/users/login'))
        self.general_form_input(
            {'username':self.credentials['email'],'password':self.credentials['password1']}
            ,form_id='login-form')
        #check user is redirected to dashboard on successful login
        self.assertIn('dashboard',self.browser.current_url)

    def submit_form(self,form_id):
        self.browser.find_element_by_id(form_id).submit()

    def fill_employee_checklist(self,redirect_url):
        self.general_form_input(data=self.employee_checklist,form_id="employee_checklist_form")
        self.assertIn(redirect_url,self.browser.current_url)



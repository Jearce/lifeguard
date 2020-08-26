from django.urls import resolve,reverse
from django.http import HttpRequest
from django.test import TestCase

from employee.models import (Transportation,
                             Employee,
                             EmployeeEducation,
                             JobHistory,
                             Position)

from employee.forms import (EducationInlineFormset,
                            JobHistoryInlineFormset)
from employee import views

from users.models import User
from lifeguard.models import Lifeguard

from utils.test.helpers import InlineFormsetManagmentFactory

class CommonSetUp(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = 'test@example.com'
        cls.password = 'asdhf33!'
        cls.new_lifeguard = {
            "already_certified":False,#new lifeguard
            "wants_to_work_for_company":True,#should be redirected to employee register page
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        cls.employee_data = {
            "home_phone":"712 634 3328",
            "who_referred_you":"A friend.",
            "transportation":"1",
            "start_date":"2020-08-09",
            "end_date":"2020-12-10",
            "work_hours_desired":"40",
            "desired_pay_rate":"17.50",
            "pool_preference":"Village Pool",
            "subdivision":"My subdivision 122",
            "work_authorization":True,
            "charged_or_arrested":False,
            "has_felony":False,
            "contract_employment_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        cls.position1 = Position.objects.create(title="Lifeguard",minimum_age=15,lifeguard_required=True)
        cls.position2 = Position.objects.create(title="Supervisor",minimum_age=18,lifeguard_required=False)
        cls.transportation = Transportation.objects.create(name="Car",description="I will drive by car")

    def setUp(self):
        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.client.login(email=self.email,password=self.password)

    def create_employee(self,applied_positions=None):
        if not applied_positions:
            #default position that requires lifeguard certificate
            applied_positions = [self.position1]

        employee = Employee(
            user=self.user,
            transportation=self.transportation,
            **{
                key:value
                for key, value in self.employee_data.items()
                if key != 'transportation' and key != 'applied_positions'}
        )
        employee.save()
        employee.applied_positions.set(applied_positions)
        return employee

class EmployeeCreateOrUpdateTest(CommonSetUp):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('employee:create'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employee:create'))
        self.assertTemplateUsed(response,'employee/employee_form.html')

    def test_create_employee(self):
        response =self.client.post(reverse('employee:create'),{**self.employee_data,"applied_positions":(1,2)})
        self.assertEqual(response.status_code,302)
        self.assertEqual(Employee.objects.count(),1)

    def test_update_employee(self):
        employee = self.create_employee()
        response =self.client.post(reverse('employee:create'),{**self.employee_data,"applied_positions":1})
        self.assertEqual(response.status_code,302)
        self.assertEqual(Employee.objects.count(),1)

class EmployeeEducationTest(CommonSetUp):
    def setUp(self):
        super().setUp()
        self.employee = self.create_employee()
        self.education_to_create = [{
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':True,
            'date_leaving_to_college':'9/10/2020',
            'employee':self.employee.pk,
            'id':'',
        }]

        #for update test
        self.previous_education = {
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':True,
            'date_leaving_to_college':'2020-09-12',
        }

        self.new_educations = [
            {
                'school_name':'Django Collegge',
                'grade_year':"Freshmen",
                'attending_college':True,
                'date_leaving_to_college':'9/10/2020',
                'employee':self.employee.pk,
                'id':'1',
            },
            {
                'school_name':'Django Collegge',
                'grade_year':"Freshmen",
                'attending_college':True,
                'date_leaving_to_college':'9/10/2020',
                'employee':self.employee.pk,
                'id':'',
            }
        ]

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('employee:education'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employee:education'))
        self.assertTemplateUsed(response,'employee/education_form.html')

    def test_create_employee_education(self):
        management_factory = InlineFormsetManagmentFactory(
            formset=EducationInlineFormset,
            extra=2,
            initial=0,
            min_num=0,
            max_num=2,
            records=self.education_to_create
        )

        education_form_data = management_factory.create_management_form()
        response = self.client.post(reverse('employee:education'),education_form_data)

        self.assertEqual(EmployeeEducation.objects.count(),1)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('employee:job_history'))

    def test_update_employee_education(self):

        EmployeeEducation.objects.create(employee=self.employee,**self.previous_education)
        self.assertEqual(EmployeeEducation.objects.count(),1)

        management_factory = InlineFormsetManagmentFactory(
            formset=EducationInlineFormset,
            extra=2,
            initial=1,
            min_num=0,
            max_num=2,
            records=self.new_educations
        )

        education_form_data = management_factory.create_management_form()
        response = self.client.post(reverse('employee:education'),education_form_data)

        self.assertEqual(response.status_code,302)
        self.assertEqual(EmployeeEducation.objects.count(),2)
        self.assertRedirects(response,reverse('employee:job_history'))

class JobHistoryTest(CommonSetUp):
    def setUp(self):
        super().setUp()
        self.create_job_history_data = [{
            "previous_employer":"Some Company",
            "job_title":"Test Job",
            "salary":"25.50",
            "start_date":"2000-06-09",
            "end_date":"2010-06-09",
            "reason_for_leaving":"The time felt right",
        }]

        self.update_job_history_data = [
            {
                "previous_employer":"Some Company",
                "job_title":"Test Job",
                "salary":"25.50",
                "start_date":"2000-06-09",
                "end_date":"2010-06-09",
                "reason_for_leaving":"The time felt right",
                "employee":'1',
                "id":'1',
            },
            {
                "previous_employer":"My School Company",
                "job_title":"Tester",
                "salary":"20.50",
                "start_date":"2010-06-09",
                "end_date":"2011-06-09",
                "reason_for_leaving":"School ended",
                "employee":'1',
                "id":''
            }
        ]

    def test_view_url_exists_at_desired_location(self):
        employee = self.create_employee()
        response = self.client.get(reverse('employee:job_history'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        employee = self.create_employee()
        response = self.client.get(reverse('employee:job_history'))
        self.assertTemplateUsed(response,'employee/job_history_form.html')

    def test_create_job_history(self):
        employee = self.create_employee()
        management_factory = InlineFormsetManagmentFactory(
            formset=JobHistoryInlineFormset,
            extra=2,
            initial=0,
            min_num=0,
            max_num=2,
            records=self.create_job_history_data
        )
        form_data = management_factory.create_management_form()
        response = self.client.post(reverse('employee:job_history'),form_data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(JobHistory.objects.count(),1)

    def test_update_job_history(self):
        employee = self.create_employee()
        JobHistory.objects.create(employee=employee,**self.create_job_history_data[0])
        management_factory = InlineFormsetManagmentFactory(
            formset=JobHistoryInlineFormset,
            extra=2,
            initial=1,
            min_num=0,
            max_num=2,
            records=self.update_job_history_data
        )
        form_data = management_factory.create_management_form()
        response = self.client.post(reverse('employee:job_history'),form_data)
        self.assertEqual(response.status_code,302)
        self.assertEqual(JobHistory.objects.count(),2)

    def test_redirect_for_applied_non_lifeguard(self):
        employee = self.create_employee(applied_positions=[self.position2])

        management_factory = InlineFormsetManagmentFactory(
            formset=JobHistoryInlineFormset,
            extra=2,
            initial=0,
            min_num=0,
            max_num=2,
            records=self.create_job_history_data
        )
        form_data = management_factory.create_management_form()

        response = self.client.post(reverse('employee:job_history'),form_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('users:dashboard'))

    def test_redirect_for_applied_lifeguard_position(self):
        employee = self.create_employee(applied_positions=[self.position1,self.position2])

        management_factory = InlineFormsetManagmentFactory(
            formset=JobHistoryInlineFormset,
            extra=2,
            initial=0,
            min_num=0,
            max_num=2,
            records=self.create_job_history_data
        )
        form_data = management_factory.create_management_form()

        response = self.client.post(reverse('employee:job_history'),form_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('lifeguard:create'))

    def test_redirect_for_already_lifeguard(self):
        lifeguard = Lifeguard.objects.create(user=self.user,**self.new_lifeguard)
        employee = self.create_employee(applied_positions=[self.position1,self.position2])

        management_factory = InlineFormsetManagmentFactory(
            formset=JobHistoryInlineFormset,
            extra=2,
            initial=0,
            min_num=0,
            max_num=2,
            records=self.create_job_history_data
        )
        form_data = management_factory.create_management_form()

        response = self.client.post(reverse('employee:job_history'),form_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('lifeguard:classes'))

class EmployeeRegistrationTest(CommonSetUp):
    def test_user_started_with_employee_registration(self):
        response = self.client.get(reverse("employee:registration"))
        self.assertEqual(response.status_code,302)
        registration_path = response.wsgi_request.session.get("registration_path")
        self.assertEqual(registration_path,"employee:create")

class EmployeeApplicationDetailTest(CommonSetUp):
    def setUp(self):
        super().setUp()
        self.employee = self.create_employee()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('employee:application_status'))
        self.assertEqual(response.status_code,200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('employee:application_status'))
        self.assertTemplateUsed(response,'employee/application_status_detail.html')

class EmployeeCheckListTest(CommonSetUp):
    def setUp(self):
        super().setUp()
        self.employee = self.create_employee()
        self.employee.is_hired = True

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('employee:checklist'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employee:checklist'))
        self.assertTemplateUsed(response,'employee/checklist_form.html')

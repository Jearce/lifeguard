from django.urls import resolve,reverse
from django.http import HttpRequest
from django.test import TestCase

from users.models import User
from lifeguard.models import Lifeguard

from employee.models import Transportation,Employee,EmployeeEducation
from employee import views
from employee.forms import EducationInlineFormset

from utils.test.helpers import InlineFormsetManagmentFactory

class CommonSetUp(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = 'test@example.com'
        cls.password = 'asdhf33!'
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)
        cls.new_lifeguard = {
            "already_certified":"N",#new lifeguard
            "wants_to_work_for_company":"Y",#should be redirected to employee register page
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        cls.employee_data = {
            "home_phone":"712 634 3328",
            "who_referred_you":"A friend.",
            "transportation":"1",
            "applied_position":'L',
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
        cls.transportation = Transportation.objects.create(name="Car",description="I will drive by car")

    def setUp(self):
        self.client.login(email=self.email,password=self.password)

class EmployeeCreateOrUpdateTest(CommonSetUp):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('employee:create'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employee:create'))
        self.assertTemplateUsed(response,'employee/employee_form.html')

    def test_employee_registration(self):
        lifeguard = Lifeguard.objects.create(user=self.user,**self.new_lifeguard)
        response =self.client.post(reverse('employee:create'),self.employee_data)
        self.assertEqual(response.status_code,302)

class EmployeeEducationTest(CommonSetUp):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = Employee.objects.create(
            user=cls.user,
            transportation=cls.transportation,
            **{
                key:value
                for key, value in cls.employee_data.items()
                if key != 'transportation'}
        )

        cls.education_to_create = [{
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':True,
            'date_leaving_to_college':'9/10/2020',
            'employee':cls.employee.pk,
            'id':'',
        }]

        #for update test
        cls.previous_education = {
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':True,
            'date_leaving_to_college':'2020-09-12',
        }

        cls.new_educations = [
            {
                'school_name':'Django Collegge',
                'grade_year':"Freshmen",
                'attending_college':True,
                'date_leaving_to_college':'9/10/2020',
                'employee':cls.employee.pk,
                'id':'1',
            },
            {
                'school_name':'Django Collegge',
                'grade_year':"Freshmen",
                'attending_college':True,
                'date_leaving_to_college':'9/10/2020',
                'employee':cls.employee.pk,
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

        self.assertEqual(EmployeeEducation.objects.count(),2)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('employee:job_history'))

class JobHistoryTest(CommonSetUp):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('employee:job_history'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employee:job_history'))
        self.assertTemplateUsed(response,'employee/job_history_form.html')

    def test_create_job_history(self):
        data = {}
        response = self.client.post(reverse('employee:job_history'),data)
        self.assertEqual(response.status_code,302)


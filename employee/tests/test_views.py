from django.urls import resolve,reverse
from django.http import HttpRequest
from django.test import TestCase
from django.contrib.sites.models import Site

from employee.models import (Transportation,
                             Employee,
                             EmployeeEducation,
                             JobHistory,
                             Position,
                             PDFFile)

from employee.forms import (EducationInlineFormset,
                            JobHistoryInlineFormset)
from employee import views
from users.models import User,EmergencyContact
from lifeguard.models import Lifeguard

from employee.tests.helpers import CommonSetUp
from utils.test.helpers import InlineFormsetManagmentFactory
from utils.test.helpers import create_emergency_contact

class EmployeeCreateOrUpdateTest(CommonSetUp):

    def test_view_url_exists_at_desired_location(self):
        self.create_emergency_contact()
        response = self.client.get(reverse('employee:create'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        self.create_emergency_contact()
        response = self.client.get(reverse('employee:create'))
        self.assertTemplateUsed(response,'employee/employee_form.html')

    def test_has_not_completed_emergency_contact_form(self):
        response = self.client.get(reverse('employee:create'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('users:emergency_contact'))

    def test_create_employee(self):
        positions = Position.objects.all()
        response =self.client.post(reverse('employee:create'),{**self.employee_data,"applied_positions":(positions[0].id,positions[0].id)})
        self.assertEqual(response.status_code,302)
        self.assertEqual(Employee.objects.count(),1)

    def test_update_employee(self):
        employee = self.create_employee()
        positions = Position.objects.all()
        response =self.client.post(reverse('employee:create'),{**self.employee_data,"applied_positions":positions[0].id})
        self.assertEqual(response.status_code,302)
        self.assertEqual(Employee.objects.count(),1)

    def create_emergency_contact(self):
        emergency_contacts = [
            {
                "name":"Mary",
                "relationship":"mom",
                "phone":"712 434 2348"
            },
            {
                "name":"Jerry",
                "relationship":"dad",
                "phone":"712 434 2348"
            }
        ]

        user_ems = []
        for em in emergency_contacts:
            user_em = EmergencyContact.objects.create(user=self.user,**em)
            user_ems.append(user_em)
        return user_ems


class EmployeeEducationTest(CommonSetUp):
    def setUp(self):
        super().setUp()
        self.employee = self.create_employee()
        self.education_to_create = [{
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':True,
            'date_leaving_to_college':'2020-09-12',
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
                'date_leaving_to_college':'2020-10-9',
                'employee':self.employee.pk,
                'id':'1',
            },
            {
                'school_name':'Django Collegge',
                'grade_year':"Freshmen",
                'attending_college':True,
                'date_leaving_to_college':'2020-10-9',
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
        #update because id is auto incremented from previous db drop in testing with postgres
        self.new_educations[0].update({"id":EmployeeEducation.objects.all()[0].id})
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
                "employee":"",
                "id":'',
            },
            {
                "previous_employer":"My School Company",
                "job_title":"Tester",
                "salary":"20.50",
                "start_date":"2010-06-09",
                "end_date":"2011-06-09",
                "reason_for_leaving":"School ended",
                "employee":"",
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
        job = JobHistory.objects.create(employee=employee,**self.create_job_history_data[0])
        self.update_job_history_data[0].update({'employee':employee.user.id})
        self.update_job_history_data[0].update({'id':job.id})
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
        create_emergency_contact(self.user)
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


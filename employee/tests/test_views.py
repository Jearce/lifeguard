from django.urls import resolve,reverse
from django.http import HttpRequest
from django.test import TestCase

from users.models import User
from lifeguard.models import Lifeguard
from employee.models import Transportation


from employee import views

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
        Transportation.objects.create(name="Car",description="I will drive by car")

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
        employee_data = {
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
        response =self.client.post(reverse('employee:create'),employee_data)
        self.assertEqual(response.status_code,302)

class EmployeeEducationTest(CommonSetUp):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('employee:education'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employee:education'))
        self.assertTemplateUsed(response,'employee/education_form.html')

    def test_employee_education(self):
        pass





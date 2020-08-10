from django.urls import resolve,reverse
from django.http import HttpRequest
from django.test import TestCase

from users.models import User
from lifeguard.models import Lifeguard

from .. import views

class EmployeeCreateOrUpdateTest(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'asdhf33!'
        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.client.login(email=self.email,password=self.password)

        self.new_lifeguard = {
            "already_certified":"N",#new lifeguard
            "wants_to_work_for_company":"Y",#should be redirected to employee register page
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('employee:create'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('employee:create'))
        self.assertTemplateUsed(response,'employee/employee_form.html')

    def test_employee_registration(self):
        lifeguard = Lifeguard.objects.create(user=self.user,**self.new_lifeguard)
        employee_data = {"home_phone":"712 634 3328"}
        response =self.client.post(reverse('employee:create'),employee_data)
        self.assertEqual(response.status_code,302)








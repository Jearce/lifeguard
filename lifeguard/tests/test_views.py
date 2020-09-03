import os
from datetime import datetime

from django.urls import resolve
from django.urls import reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from .. import views
from users.models import User
from employee.models import Employee,Transportation,Position
from ..models import LifeguardClass,Enroll,Lifeguard
from lifeguard.tests.helpers import set_up_time,LifeguardFactory

from dateutil.relativedelta import relativedelta

class BaseUserSetUp(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'sdfh328j!'
        self.user = User.objects.create_user(email=self.email,password=self.password)

class HomeViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response,'home.html')

class LifeguardCreateTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.user_login = self.client.login(email=self.email,password=self.password)
        self.new_working_lifeguard = {
            "already_certified":False,#new lifeguard
            "wants_to_work_for_company":True,#should be redirected to employee register page
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        self.certified_working_lifeguard =  {
            "already_certified":True,
            "wants_to_work_for_company":True,
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        self.new_lifeguard = {
            "already_certified":False,
            "wants_to_work_for_company":False,
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        self.employee_data = {
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
        self.transportation = Transportation.objects.create(name="Car",description="I will drive by car")
        self.position1 = Position.objects.create(title="Lifeguard",minimum_age=15,lifeguard_required=True)
        self.position2 = Position.objects.create(title="Supervisor",minimum_age=18,lifeguard_required=False)


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('lifeguard:create'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('lifeguard:create'))
        self.assertTemplateUsed(response,'lifeguard/lifeguard_form.html')

    def test_lifeguard_create(self):
        response = self.client.post(reverse('lifeguard:create'),self.new_working_lifeguard)
        self.assertEqual(response.status_code,302)

    def test_lifeguard_update(self):
        #user is already a lifeguard
        Lifeguard.objects.create(user=self.user,**self.new_working_lifeguard)

        response = self.client.post(reverse('lifeguard:create'),self.certified_working_lifeguard)
        self.assertEqual(Lifeguard.objects.count(),1)
        self.assertEqual(response.status_code,302)

    def test_redirect_for_already_certified_lifeguard(self):
        response = self.client.post(reverse('lifeguard:create'),self.certified_working_lifeguard)
        self.assertRedirects(response,reverse('lifeguard:already_certified'))

    def test_redirect_for_new_lifeguard_that_wants_to_work(self):
        response = self.client.post(reverse('lifeguard:create'),self.new_working_lifeguard)
        self.assertRedirects(response,reverse('employee:create'))

    def test_redirect_for_new_lifeguard(self):
        response = self.client.post(reverse('lifeguard:create'),self.new_lifeguard)
        self.assertRedirects(response,reverse('lifeguard:classes'))

    def test_redirect_for_lifeguard_who_applied_as_employee(self):
        employee = Employee(
            user=self.user,
            transportation=self.transportation,
            **{
                key:value
                for key, value in self.employee_data.items()
                if key != 'transportation' and key != 'applied_positions'
            }
        )
        employee.save()
        employee.applied_positions.set([self.position1,self.position2])
        response = self.client.post(reverse('lifeguard:create'),self.new_lifeguard)
        self.assertRedirects(response,reverse('lifeguard:classes'))

class LifeguardAlreadyCertifiedTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.user_login = self.client.login(email=self.email,password=self.password)
        self.certified_lifeguard = {
            "already_certified":True,
            "wants_to_work_for_company":False,
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        self.working_certified_lifeguard = {
            "already_certified":True,
            "wants_to_work_for_company":True,
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
    def test_view_url_exists_at_desired_location(self):
        self.create_lifeguard(self.certified_lifeguard)
        response = self.client.get(reverse('lifeguard:already_certified'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        self.create_lifeguard(self.certified_lifeguard)
        response = self.client.get(reverse('lifeguard:already_certified'))
        self.assertTemplateUsed(response,'lifeguard/already_certified_form.html')

    def test_already_certified(self):
        response = self.submit_certificate('lifeguard/tests/certificate.pdf',self.certified_lifeguard)
        self.assertEqual(response.status_code,302)

    def test_redirect_for_certified_lifeguard(self):
        response = self.submit_certificate('lifeguard/tests/certificate.pdf',self.certified_lifeguard)
        self.assertRedirects(response,reverse('lifeguard:classes'))

    def test_redirect_for_working_certified_lifeguard(self):
        response = self.submit_certificate('lifeguard/tests/certificate.pdf',self.working_certified_lifeguard)
        self.assertRedirects(response,reverse('employee:create'))


    def create_lifeguard(self,data):
        Lifeguard.objects.create(user=self.user,**data)

    def submit_certificate(self,path_to_certificate,lifeguard_data):
        self.create_lifeguard(lifeguard_data)
        with open(path_to_certificate,'rb') as pdf:
            response = self.client.post(reverse('lifeguard:already_certified'),{'last_certified':'2000-06-09','certification':pdf})
        return response

class LifeguardClassesTest(BaseUserSetUp):
    fixtures = ['classes.json']
    def setUp(self):
        super().setUp()
        user_login = self.client.login(email=self.email, password=self.password)
        self.lifeguard_data = {
            "already_certified":False,
            "wants_to_work_for_company":True,
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('lifeguard:classes'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('lifeguard:classes'))
        self.assertTemplateUsed(response,'lifeguard/classes.html')

    def test_can_enroll_in_class(self):
        Lifeguard.objects.create(user=self.user,**self.lifeguard_data)
        classes = LifeguardClass.objects.all()
        response = self.client.post(reverse('lifeguard:classes',kwargs={'pk':classes[0].id}))
        self.assertEqual(response.status_code,302)
        self.assertEqual(Enroll.objects.all().count(),1)
        self.assertRedirects(response,reverse('lifeguard:payment'))

    def test_shows_only_review_classes(self):
        needs_review_time = set_up_time(years=2,days=15)
        lifeguard = LifeguardFactory(user=self.user,last_certified=needs_review_time).create()
        self.assertEqual(Lifeguard.objects.count(),1)

        response = self.client.get(reverse('lifeguard:classes'))
        self.assertTrue(all(lgclass.is_review for lgclass in response.context['classes']))

    def test_shows_only_certified_and_nonreview_classes(self):
        needs_refresher_time = set_up_time(years=1,days=15)
        lifeguard = LifeguardFactory(user=self.user,last_certified=needs_refresher_time).create()
        self.assertEqual(Lifeguard.objects.count(),1)

        response = self.client.get(reverse('lifeguard:classes'))
        self.assertTrue(
            all(
                lgclass.lifeguard_certified_required and not lgclass.is_review
                for lgclass in response.context['classes']
            )
        )

    def test_not_lifeguard_yet_cant_enroll(self):
        classes = LifeguardClass.objects.all()
        response = self.client.post(reverse('lifeguard:classes',kwargs={'pk':classes[0].id}))
        self.assertEqual(response.status_code,302)
        self.assertEqual(Enroll.objects.all().count(),0)
        self.assertRedirects(response,reverse('lifeguard:create'))


class LifeguardRegistrationTest(BaseUserSetUp):
    def setUp(self):
        super().setUp()
        self.client.login(email=self.email,password=self.password)

    def test_user_started_with_lifeguard_registration(self):
        response = self.client.get(reverse("lifeguard:registration"))
        self.assertEqual(response.status_code,302)
        registration_path = response.wsgi_request.session.get("registration_path")
        self.assertEqual(registration_path,"lifeguard:create")




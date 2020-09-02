from django.test import TestCase
from employee import forms
from django.conf import settings

from employee.tests.helpers import CommonSetUp

BASE_DIR = settings.BASE_DIR

class EmployeeEducationFormTest(TestCase):
    def test_forget_to_finish_filling_out_date_leaving_to_college(self):
        data = {
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':True,
            'date_leaving_to_college':'',
        }
        form = forms.EducationForm(data=data)
        errors = form.errors
        self.assertEqual(errors["date_leaving_to_college"],["Please fill out the date you will be leaving."])

    def test_skipped_attending_college_and_filled_out_date_leaving(self):
        data = {
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':'',
            'date_leaving_to_college':'2020-08-21',
        }
        form = forms.EducationForm(data=data)
        errors = form.errors
        self.assertEqual(errors["attending_college"],["This field is required."])

class EmployeeCheckListFormTest(CommonSetUp):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ChecklistForm = forms.ChecklistForm

    def setUp(self):
        super().setUp()
        #already submitted application
        self.employee = self.create_employee()
        self.employee.is_hired = True
        self.employee.save()
        self.checklist_data = {
            "banking_name":"Banking 123",
            "account_type":"S",#choose savings
            "account_number":"19282739",
            "savings_number":"1728327",
            "email_address":self.user.email,
            "auth_signature":"Larry Johnson",
            "awknowledgement_form_signature":"Larry Johnson",
        }

        self.checklist_files = {
            "photo_id":f"{self.path_to_test_files}/photoid.pdf",
            "social_security_card":f"{self.path_to_test_files}/social.pdf",
            "social_security_number":"444-44-444",
            "birth_certificate":f"{self.path_to_test_files}/birthcertificate.pdf",
            "w4":f"{self.path_to_test_files}/w4.pdf",
            "i9":f"{self.path_to_test_files}/i9.pdf",
            "workers_comp":f"{self.path_to_test_files}/workers_comp.pdf",
            "vaccination_record":f"{self.path_to_test_files}/vaccination.pdf",
        }



    def test_email_address_already_filled_in(self):
        form = self.ChecklistForm(user=self.user)
        self.assertEqual(self.user.email,form.initial["email_address"])

    def test_cannot_submit_vaccination_record_and_fill_wavier(self):
        #sign wavier to
        self.checklist_data["hepB_waiver_signature"] = "Larry Johnson"
        form = self.ChecklistForm(self.user,self.checklist_data,files=self.checklist_files)
        self.assertFalse(form.is_valid())
        self.assertIn(form.error_messages["invalid_wavier_and_record"],form.non_field_errors())
        #self.assertEqual(errors["hepB_waiver_signature"]







from django.test import TestCase
from employee import forms

from employee.tests.helpers import CommonSetUp

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
    def setUp(self):
        super().setUp()
        #already submitted application
        self.employee = self.create_employee()
        self.employee.is_hired = True
        self.employee.save()

    def test_email_address_already_filled_in(self):
        form = forms.ChecklistForm(user=self.user)
        self.assertEqual(self.user.email,form.fields['email_address'].initial)

    def test_cannot_fill_wavier_and_submit_vaccination_record(self):



from django.test import TestCase
from employee.forms import EducationForm

class EmployeeEducationFormTest(TestCase):
    def test_forget_to_finish_filling_out_date_leaving_to_college(self):
        data = {
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':True,
            'date_leaving_to_college':'',
        }
        form = EducationForm(data=data)
        errors = form.errors
        self.assertEqual(errors["date_leaving_to_college"],["Please fill out the date you will be leaving."])

    def test_skipped_attending_college_and_filled_out_date_leaving(self):
        data = {
            'school_name':'Django High School',
            'grade_year':"12th grade",
            'attending_college':'',
            'date_leaving_to_college':'2020-08-21',
        }
        form = EducationForm(data=data)
        errors = form.errors
        self.assertEqual(errors["attending_college"],["This field is required."])





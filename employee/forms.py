from django.forms import (ModelForm,
                          Select,
                          DateInput,
                          RadioSelect,
                          CheckboxSelectMultiple,
                          inlineformset_factory)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Submit,HTML


from .models import Employee,EmployeeEducation,JobHistory,Checklist


BOOLEAN_CHOICES = [(True,"Yes"),(False,"No")]
class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        exclude = ('user',)
        widgets = {
            'applied_position':RadioSelect,
            'start_date':DateInput(attrs={'type':'date'}),
            'end_date':DateInput(attrs={'type':'date'}),
            "applied_positions":CheckboxSelectMultiple,
            "work_authorization":RadioSelect,
            "charged_or_arrested":RadioSelect,
            "has_felony":RadioSelect,
        }

class EducationForm(ModelForm):
    class Meta:
        model = EmployeeEducation
        fields = [
            "school_name",
            "grade_year",
            "attending_college",
            "date_leaving_to_college",
        ]
        widgets = {
            "date_leaving_to_college":DateInput(attrs={'type':'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        attending = cleaned_data["attending_college"]
        date_leaving = cleaned_data["date_leaving_to_college"]

        if attending and not date_leaving:
            self.add_error('date_leaving_to_college',"Please fill out the date you will be leaving.")

        elif date_leaving and not attending:
            self.add_error("attending_college","This field is required.")

class ChecklistForm(ModelForm):
    class Meta:
        model = Checklist
        fields = [
            'photo_id',
            'social_security_card',
            'social_security_number',
            'birth_certificate',
            'w2',
            'i9',
            'workers_comp',
            'hepB_vaccine_signature',
            'banking_name',
            'account_type',
            'account_number',
            'savings_number',
            'email_address',
            'auth_signature',
        ]

        widgets = {
            'account_type':RadioSelect,

        }

        labels = {
            "banking_name":"Banking or Financial Institution Name:",
            "account_type":"Account Type: Select One Account:",
            "email_address":"Email Address (to receive pay stubs):",
            "auth_signature":"Authorize Signature",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML("<h3>Employee Direct Deposit Authorization</h3>"),
                'banking_name',
                'account_type',
                'account_number',
                'savings_number',
                'email_address',
                'auth_signature',
            )
        )

class JobHistoryForm(ModelForm):
    class Meta:
        model = JobHistory
        fields = [
            "previous_employer",
            "job_title",
            "salary",
            "start_date",
            "end_date",
            "reason_for_leaving"
        ]
        widgets = {
            "start_date":DateInput(attrs={'type':'date'}),
            "end_date":DateInput(attrs={'type':'date'})
        }

EducationInlineFormset = inlineformset_factory(
    Employee,
    EmployeeEducation,
    form=EducationForm,
    extra=2,
    max_num=2,
    can_delete=False,
    can_order=False
)

JobHistoryInlineFormset = inlineformset_factory(
    Employee,
    JobHistory,
    form=JobHistoryForm,
    extra=2,
    max_num=2,
    can_delete=False,
    can_order=False
)


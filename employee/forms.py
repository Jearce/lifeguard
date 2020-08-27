from django.forms import (ModelForm,
                          Select,
                          DateInput,
                          RadioSelect,
                          CheckboxSelectMultiple,
                          inlineformset_factory)

from django.contrib.sites.models import Site

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Submit,HTML


from .models import Employee,EmployeeEducation,JobHistory,Checklist,PDFFile


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

def render_download_html(url,name):
    return f"You can download <a href='{url}'>{name}</a> here."

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
            "hepB_vaccine_signature":"Employee Signature",
            "banking_name":"Banking or Financial Institution Name:",
            "account_type":"Account Type: Select One Account",
            "email_address":"Email Address (to receive pay stubs):",
            "auth_signature":"Authorize Signature",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pdfs = Site.objects.get_current().pdffile

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'photo_id',
            'social_security_card',
            'social_security_number',
            'birth_certificate',
            Div(
                HTML(render_download_html(pdfs.w4.url,"W4")),
                'w2',
                HTML(render_download_html(pdfs.i9.url,"I9")),
                'i9',
                HTML(render_download_html(pdfs.workers_comp.url,"Workers Comp")),
                'workers_comp',
            ),
            Div(
                HTML("""
                     <h4>Hepatitis B Vaccine Waiver</h4>
                     <p>Declination Statement</p>
                     <p>
                     I understand that due to my occupational
                     exposure to blood or other potentially
                     infectious materials I may be at risk of acquiring
                     hepatitis B virus (HPV) infection. I have been
                     given the opportunity to be vaccinated with hepatitis
                     B vaccine, at no charge to me; however, I decline hepatitis
                     B vaccination at this time. I understand that by declining this vaccine
                     I continue  to be at a risk of acquiring hepatitis B,
                     a serious disease. If, in the future I continue to have
                     occupational exposure to bllod or other potentially
                     infectious materials and I want to be vaccinated with
                     hepatitis B vaccine, I can recieve the vaccination series
                     at no charge to me.
                     </p>
                     """),
                'hepB_vaccine_signature',
                css_id="hepVaccineWaiver",
            ),
            Div(
                HTML("<h4>Employee Direct Deposit Authorization</h4>"),
                'banking_name',
                'account_type',
                'account_number',
                'savings_number',
                'email_address',
                HTML("""
                     <p>Authorization:</p>
                     <p>
                     This authorizes Gulf Coast Aquatics, Inc. to send credit
                     entries (and appropriate debit and adjustment entries),
                     electronically or by any other commercially accepted
                     method, to my (our) account indicated above and to other
                     accounts I (we) identify in the future (the "Account").
                     This authorizes the financial institution holding
                     the Account to post all such entries. I agree that
                     the ACH transactions  authorized herein shall comply
                     with all the applicable U.S. Laws. This authorization
                     will be in effect until the company receives a written
                     termination notice from myself and has a reasonable
                     opportunity to act on it.
                     </p>
                     """),
                'auth_signature',
                css_id="directDeposit"
            ),
        Submit('','Submit'),
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


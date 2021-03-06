from django import forms
from django.forms import (ModelForm,
                          CheckboxInput,
                          Select,
                          DateInput,
                          RadioSelect,
                          CheckboxSelectMultiple,
                          inlineformset_factory)

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Submit,HTML,Fieldset,Field


from .models import Employee,EmployeeEducation,JobHistory,Checklist,PDFFile


BOOLEAN_CHOICES = [(True,"Yes"),(False,"No")]
class EmployeeForm(ModelForm):
    class Meta:
        long_labels = {
            "work_authorization":"Are you legally authorized to work in the United States?",
            "charged_or_arrested_resolved":
            """
            Have you ever been charged, detained, or arrested for a felony or
            sex crime that was resolved by conviction, probation, deferred
            adjudication, court ordered community supervision, or pretrial diversion?
            """,
            "charged_or_arrested_not_resolved":
            """
            Have you ever been charged, detained, or arrested for a felony
            or sex-related crime that has not been resolved by any method?
            """,
        }

        model = Employee
        fields = [
            'home_phone',
            'who_referred_you',
            'transportation',
            'applied_positions',
            'start_date',
            'end_date',
            'work_hours_desired',
            'desired_pay_rate',
            'pool_preference',
            'subdivision',
            'work_authorization',
            'charged_or_arrested_resolved',
            'charged_or_arrested_not_resolved',
            'contract_employment_agreement',
            'electronic_signature'
        ]

        widgets = {
            'applied_position':RadioSelect,
            'start_date':DateInput(attrs={'type':'date'}),
            'end_date':DateInput(attrs={'type':'date'}),
            "applied_positions":CheckboxSelectMultiple,
            "work_authorization":RadioSelect,
            "charged_or_arrested_resolved":RadioSelect,
            "charged_or_arrested_not_resolved":RadioSelect,
        }

        labels = {
            "start_date":"Date available to start",
            'ending_date':"Ending date - This is not official. A notice is still required.",
            "work_hours_desired":"Number of hours desired per week",
            "contract_employment_agreement":"I agree",
            'work_authorization':long_labels['work_authorization'],
            'charged_or_arrested_resolved':long_labels['charged_or_arrested_resolved'],
            'charged_or_arrested_not_resolved':long_labels['charged_or_arrested_not_resolved'],
            'contract_employment_agreement':'I agree',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "employee_form"
        self.helper.form_class = "w-25 center-form isolate-form"
        self.helper.layout = Layout(
            'home_phone',
            'who_referred_you',
            'transportation',
            'applied_positions',
            'start_date',
            'end_date',
            'work_hours_desired',
            'desired_pay_rate',
            'pool_preference',
            'subdivision',
            'work_authorization',
            'charged_or_arrested_resolved',
            'charged_or_arrested_not_resolved',
            HTML("""
                 <p>
                   I understand that this application is not a contract of employment.
                   I understand that false or misleading information given in my application
                   or interview(s) will result in termination. I understand that in the event
                   of employment, employment relationship is terminable at will and
                   is not governed by an employment contract. I also understand that
                   the use of illegal drugs or alcohol is prohibited during employment
                   and is grounds for immediate termination. In the event that I am employed,
                   I agree and abide by all policies and standards of
                   Gulf Coast Aquatics, Inc.Gulf Coast Aquatics, Inc is an
                   equal opportunity employer.*
                 </p>
                 """),
            'contract_employment_agreement',
            'electronic_signature',
            Submit('','Submit',css_class="btn btn-outline-primary btn-block btn-lg")
        )

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

def render_html(url,name):
    return f"(<i>You can download the <a href='{url}'>{name}</a> form here.</i>)"

class ChecklistForm(ModelForm):

    need_to_fill_out_wavier = forms.BooleanField(
        label="I have not recieved or do not want a vaccination for Hep B.",
        required=False,
    )

    error_messages = {
        "invalid_wavier_and_record":"""You cannot submit a Hep B vaccine
        record and sign the Hep B waiver. Please choose one or the other.""",
    }

    class Meta:
        model = Checklist
        fields = [
            'photo_id',
            'birth_certificate',
            'social_security_card',
            'social_security_number',
            'w4',
            'i9',
            'workers_comp',
            "need_to_fill_out_wavier",
            'vaccination_record',
            'hepB_waiver_signature',
            'banking_name',
            'account_type',
            'account_number',
            'router_number',
            'email_address',
            'auth_signature',
            'awknowledgement_form_signature',
        ]

        widgets = {
            "need_to_fill_out_wavier":CheckboxInput,
        }

        labels = {
            "w4":"",
            "i9":"",
            "router_number":"",
            "workers_comp":"",
            "vaccination_record":"Hepatitis B Vaccine Record",
            'birth_certificate':"Birth certificate - ONLY if you are 15",
            "hepB_waiver_signature":"Employee Signature",
            "banking_name":"Banking or Financial Institution Name:",
            "account_type":"Account Type: Select One Account",
            "email_address":"Email Address (to receive pay stubs):",
            "auth_signature":"Authorize Signature",
            "awknowledgement_form_signature":"Signature",
        }

    def __init__(self,user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.initial["email_address"] = user.email

            signed_wavier = user.employee.checklist.hepB_waiver_signature
            self.initial["need_to_fill_out_wavier"] = True if signed_wavier else False


        pdfs = Site.objects.get_current().pdffile

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "center-form"
        self.helper.form_id = "employee_checklist_form"
        self.helper.layout = Layout(
            Div(
                HTML("<h4>Identification</h4>"),
                Div(
                    Div('photo_id',css_class="form-group col"),
                    Div('birth_certificate',css_class="form-group col"),
                    css_class="form-row"
                ),
                Div(
                    Div('social_security_number',css_class="form-group col"),
                    Div('social_security_card',css_class="form-group col"),
                    css_class="form-row"
                ),
                HTML("<p><b>Note</b> photo identification can include: drivers license, passport, picture id, or student id.</p>"),
                css_class = "isolate-form"
            ),
            Div(
                HTML("<h4>W4, I-9, & Workers Compensation Forms</h4>"),
                Div(
                    HTML("W4 Form " + render_html(pdfs.w4.url,"W4")),
                    'w4',
                    HTML(
                        "I-9 Employee ID Verification Form "+
                        render_html(pdfs.i9.url,"I9")
                    ),
                    'i9',
                    HTML(
                        "Employee Acknowledgement of Workers' Compensation Network "+
                        render_html(pdfs.workers_comp.url,"Workers Comp")
                    ),
                    'workers_comp',
                ),
                css_class="isolate-form"
            ),
            Div(
                HTML("""
                     <h4>Hepatitis B Vaccination Record</h4>
                     <p>
                     Your vaccination record needs to have <b>Hapatitis B
                     vaccine</b> listed.
                     </p>
                     """),
                "need_to_fill_out_wavier",
                Field("vaccination_record",id="id_vaccination_record"),
                css_class="isolate-form",
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
                     occupational exposure to blood or other potentially
                     infectious materials and I want to be vaccinated with
                     hepatitis B vaccine, I can recieve the vaccination series
                     at no charge to me.
                     </p>
                     """),
                'hepB_waiver_signature',
                css_id="hepVaccineWaiver",
                css_class="isolate-form",
            ),
        Div(
            HTML("<h4>Employee Direct Deposit Authorization</h4>"),
            'banking_name',
            'account_type',
            'account_number',
            Div(HTML("Routing number (<a href='https://www.magnifymoney.com/blog/banking/routing-number/'>How to find routing number</a>)"),"router_number"),
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
            css_id="directDeposit",
            css_class="isolate-form"
        ),
        Div(
            HTML("""
                 <h4>Release Form</h4>
                 <p>
                 <b>I HAVE READ AND UNDERSTAND THE SEASONAL
                 EMPLOYEE HANDBOOK & SAFETY INFORMATION.</b>
                 I will abide by all rules, regulations, policies,
                 and procedures throughout my employment with Gulf Coast
                 Aquatics,Inc. Furthermore, I acknowledge that violations
                 of any Gulf Coast Aquatics, Inc. rules and regulations
                 could result in disciplinary action and/or termination of
                 my employment.
                 </p>

                 <p>
                 I understand it is my responsibility to attend In-Service
                 training throughout my employment with Gulf Coast
                 Aquatics, Inc.
                 </p>

                 <p>I will always conduct myself in a professional manner
                 throughout my employment with Gulf Coast Aquatics, Inc.</p>

                 <p>
                 I understand that if I do not submit a 2-week notice when
                 quitting, I will not be eligible for rehire.
                 </p>

                 <p>
                 I have read and received a copy of “Employee Acknowledgement
                 of Worker’s Compensation Network”.
                 </p>
                 """),
            "awknowledgement_form_signature",
            css_class="isolate-form"
        ),
        Submit('','Submit',css_class="btn-lg btn-block"),
        )


    def clean(self):
        cleaned_data = super().clean()

        wavier_signature = cleaned_data["hepB_waiver_signature"]
        vacc_record = self.files.get("vaccination_record")

        if vacc_record and wavier_signature:
            raise ValidationError(
                self.error_messages["invalid_wavier_and_record"],
                code="invalid_wavier_and_record"
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


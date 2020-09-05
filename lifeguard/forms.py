from django.forms import ModelForm
from django import forms
from lifeguard.models import Lifeguard

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Submit,Field,Button,HTML


class LifeguardCertifiedForm(ModelForm):
    class Meta:
        model = Lifeguard
        fields = ['last_certified','certification']
        widgets = {
            'last_certified':forms.DateInput(attrs={'type':'date'})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "already_certified_form"
        self.helper.form_class = "w-25 center-form isolate-form"
        self.helper.add_input(
            Submit('','Submit',css_class="btn btn-outline-primary btn-block btn-lg")
        )

class LifeguardForm(ModelForm):
    class Meta:
        model = Lifeguard
        fields = [
            'already_certified',
            'wants_to_work_for_company',
            'payment_agreement',
            'payment_agreement_signature',
            'no_refunds_agreement',
            'electronic_signature'
        ]

        widgets = {
            'already_certified':forms.RadioSelect,
            'wants_to_work_for_company':forms.RadioSelect,

        }

        labels = {
            'payment_agreement':'I understand and agree',
            'payment_agreement_signature':'Your name',
            'no_refunds_agreement':'I agree',
        }

    def __init__(self,user=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_employee:
            self.initial['wants_to_work_for_company'] = True

        self.helper = FormHelper()
        self.helper.form_id = "lifeguard_form"
        self.helper.form_class="center-form isolate-form"
        self.helper.layout = Layout(
            Field('already_certified'),
            Field('wants_to_work_for_company'),
            HTML("""
                 <p><b>NOTE:</b> Gulf Coast Aquatics
                 American Red Cross courses are <b>ONLY</b>
                 discounted for those intending to work with
                 us for the summer. All others will be charged
                 <b>FULL</b> cost of the course, failure to pay
                 this amount online will result in billing for the
                 balance on your account on the first day of the
                 course prior to starting.</p>
                 <p>Please check that you have read and
                 understand the above statement and then sign your
                 name below.</p>
                 """),
            Field("payment_agreement"),
            Field("payment_agreement_signature"),
            HTML("""
                 <p>I understand there are no refunds for this course
                 once the course begins which includes if I do not pass
                 the prerequisite requirements. I understand if I am
                 unable to pass the prerequisites, I will be given the
                 opportunity to try again one other time in a later
                 available class. Students must pass the prerequisite
                 skills in order to continue in the class.</p>
                 """),
            Field("no_refunds_agreement"),
            Field("electronic_signature"),
            Submit('','Submit',css_class="btn btn-outline-primary btn-block btn-lg"),
        )

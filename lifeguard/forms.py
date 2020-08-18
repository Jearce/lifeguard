from django.forms import ModelForm,SelectDateWidget,DateInput
from .models import Lifeguard

class LifeguardCertifiedForm(ModelForm):
    class Meta:
        model = Lifeguard
        fields = ['last_certified','certification']
        widgets = {
            'last_certified':DateInput(attrs={'type':'date'})
        }

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

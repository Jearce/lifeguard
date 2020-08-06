from django.forms import ModelForm,SelectDateWidget,DateInput
from .models import Lifeguard

class LifeguardCertifiedForm(ModelForm):
    class Meta:
        model = Lifeguard
        fields = ['last_certified','certification']
        widgets = {
            'last_certified':DateInput(attrs={'type':'date'})
        }


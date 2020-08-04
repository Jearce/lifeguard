from django.forms import ModelForm,modelformset_factory
from .models import EmergencyContact

class EmergencyContactForm(ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name','relationship','phone']

EmergencyContactFormSet = modelformset_factory(EmergencyContact,fields=('name','relationship','phone'),extra=2,)

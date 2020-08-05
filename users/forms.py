from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import ModelForm,modelformset_factory,inlineformset_factory
from .models import EmergencyContact,User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

class EmergencyContactForm(ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name','relationship','phone']

EmergencyContactFormSet = modelformset_factory(EmergencyContact,fields=('name','relationship','phone'),extra=2,max_num=2)
EmergencyContactInlineFormSet = inlineformset_factory(User,EmergencyContact,fields=('name','relationship','phone'),extra=2,max_num=2,can_order=False)

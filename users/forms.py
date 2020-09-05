from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import ModelForm,modelformset_factory,inlineformset_factory,DateInput
from .models import EmergencyContact,User
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Submit,Field,Button

class CustomUserCreationForm(UserCreationForm):
    street1 = forms.CharField(max_length=255)
    street2 = forms.CharField(required=False,max_length=255)
    city = forms.CharField(max_length=255)
    state = forms.CharField(max_length=255)
    zip = forms.CharField(max_length=255)

    class Meta(UserCreationForm):
        model = User
        fields = ['email','first_name', 'last_name','phone','dob']
        widgets = {
            "dob":DateInput(attrs={'type':'date'})
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "signup_form"
        self.helper.form_class = "center-form isolate-form"
        self.helper.layout = Layout(
            Div("email",css_class="form-group"),
            Div(
                Div("first_name",css_class="form-group col"),
                Div("last_name",css_class="form-group col"),
                css_class="form-row"
            ),
            Div("phone",css_class="form-group"),
            Div("dob",css_class="form-group"),
            Div("street1",css_class="form-group"),
            Div("street2",css_class="form-group"),
            Div(
                Div("city",css_class="col-md-6 mb-3"),
                Div("state",css_class="col-md-3 mb-3"),
                Div("zip",css_class="col-md-3 mb-3"),
                css_class="form-row"
            ),

            Div("password1",css_class="form-group"),
            Div("password2",css_class="form-group"),
            Submit('','Submit')
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

class EmergencyContactForm(ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name','relationship','phone']

class ContactInformationForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','phone','dob']
        widgets = {
            "dob":DateInput(attrs={'type':'date'})
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "center-form"
        self.helper.form_id = "contact_information_form"
        self.helper.layout = Layout(
            Div("email",css_class="form-group"),
            Div(
                Div("first_name",css_class="form-group col"),
                Div("last_name",css_class="form-group col"),
                css_class="form-row"
            ),
            Div("phone",css_class="form-group"),
            Div("dob",css_class="form-group"),
            Submit('','Submit')
        )

EmergencyContactFormSet = modelformset_factory(
    EmergencyContact,
    fields=('name','relationship','phone'),
    extra=2,
    max_num=2
)

EmergencyContactInlineFormSet = inlineformset_factory(
    User,
    EmergencyContact,
    fields=('name','relationship','phone'),
    extra=2,
    max_num=2,
    can_order=False,
    can_delete=False,
)

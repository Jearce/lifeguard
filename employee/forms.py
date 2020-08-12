from django.forms import (ModelForm,
                          DateInput,
                          RadioSelect,
                          CheckboxSelectMultiple,
                          inlineformset_factory)

from .models import Employee,EmployeeEducation


BOOLEAN_CHOICES = [(True,"Yes"),(False,"No")]
class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        exclude = ('user',)
        widgets = {
            'applied_position':RadioSelect,
            'start_date':DateInput(attrs={'type':'date'}),
            'end_date':DateInput(attrs={'type':'date'}),
            "work_authorization":RadioSelect,
            "charged_or_arrested":RadioSelect,
            "has_felony":RadioSelect,
        }

class EducationForm(ModelForm):
    class Meta:
        model = EmployeeEducation
        exclude = ('employee',)

EducationInlineFormset = inlineformset_factory(
    Employee,
    EmployeeEducation,
    form=EducationForm,
    extra=2,
    max_num=2,
    can_delete=False,
    can_order=False
)

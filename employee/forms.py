from django.forms import (ModelForm,
                          DateInput,
                          RadioSelect,
                          CheckboxSelectMultiple,
                          inlineformset_factory)

from .models import Employee,EmployeeEducation,JobHistory


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

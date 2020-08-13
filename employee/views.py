from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView

from .models import Employee,EmployeeEducation,JobHistory

from .forms import EmployeeForm,EducationInlineFormset,EducationForm,JobHistoryForm,JobHistoryInlineFormset

class InlineFormSetUpdateOrCreateViewMixin:
    def get_object(self):
        obj = self.parent_model.objects.get(user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        formset = self.formset(instance=self.get_object())
        context['formset'] = formset
        return context

    def post(self, request,*args,**kwargs):
        formset = self.formset(
            request.POST,
            instance=self.get_object()
        )
        if formset.is_valid():
            formset.save()
            return self.form_valid(formset)
        return render(request,self.template_name,context={'formset':formset})

# Create your views here.
class EmployeeCreateOrUpdate(UpdateView):
    form_class = EmployeeForm
    template_name = 'employee/employee_form.html'

    def get_object(self):
        user = self.request.user
        try:
            obj = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            obj = Employee(user=user)
        return obj

    def get_success_url(self):
        return reverse_lazy('employee:education')


class EmployeeEducation(InlineFormSetUpdateOrCreateViewMixin,UpdateView):
    model = EmployeeEducation
    template_name = 'employee/education_form.html'
    form_class = EducationForm
    parent_model = Employee
    formset = EducationInlineFormset

    def get_success_url(self):
        return reverse_lazy('employee:job_history')


class JobHistory(InlineFormSetUpdateOrCreateViewMixin,UpdateView):
    model = JobHistory
    parent_model = Employee
    form_class = JobHistoryForm
    formset = JobHistoryInlineFormset
    template_name = 'employee/job_history_form.html'

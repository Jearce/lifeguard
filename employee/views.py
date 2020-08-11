from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView

from .models import Employee

from .forms import EmployeeForm

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

class EmployeeEducation(TemplateView):
    template_name = 'employee/education_form.html'

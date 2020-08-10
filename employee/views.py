from django.shortcuts import render
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
            obj = Employee.objects.get(pk=user)
        except Employee.DoesNotExist:
            obj = Employee(user)
        return obj

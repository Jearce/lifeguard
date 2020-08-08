from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView

# Create your views here.
class EmployeeUpdate(TemplateView):
    template_name = 'employee/employee_form.html'

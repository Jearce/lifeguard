from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required

from .models import Employee,EmployeeEducation,JobHistory,Checklist,Position

from .forms import (EmployeeForm,
                    EducationInlineFormset,
                    EducationForm,
                    JobHistoryForm,
                    JobHistoryInlineFormset,
                    ChecklistForm)

class InlineFormSetViewMixin:
    parent_model = None
    formset = None

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
class EmployeeCreateOrUpdate(LoginRequiredMixin,UpdateView):
    form_class = EmployeeForm
    template_name = 'employee/employee_form.html'

    def get(self, request,*args,**kwargs):
        user = self.request.user
        emergency_contacts = user.emergencycontact_set.all()
        if not emergency_contacts.exists():
            return redirect('users:emergency_contact')
        return super().get(request,*args,**kwargs)

    def get_object(self):
        user = self.request.user
        try:
            obj = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            obj = Employee(user=user)
        return obj

    def get_success_url(self):
        return reverse_lazy('employee:education')

class EmployeeEducation(LoginRequiredMixin,InlineFormSetViewMixin,UpdateView):
    parent_model = Employee
    model = EmployeeEducation
    form_class = EducationForm
    formset = EducationInlineFormset
    template_name = 'employee/education_form.html'

    def get_success_url(self):
        return reverse_lazy('employee:job_history')

class JobHistory(LoginRequiredMixin,InlineFormSetViewMixin,UpdateView):
    model = JobHistory
    parent_model = Employee
    form_class = JobHistoryForm
    formset = JobHistoryInlineFormset
    template_name = 'employee/job_history_form.html'

    def get_success_url(self):
        #check if user applied to a position that requires a lifeguard certification
        user = self.request.user
        if user.is_lifeguard:
            return reverse_lazy('lifeguard:classes')
        elif user.employee.applied_to_lifeguard_position():
            return reverse_lazy('lifeguard:create')
        return reverse_lazy('users:dashboard')

class ApplicationStatus(LoginRequiredMixin,DetailView):
    template_name = 'employee/application_status_detail.html'
    def get_object(self):
        return self.request.user.employee

class EmployeeChecklist(LoginRequiredMixin,UpdateView):
    form_class = ChecklistForm
    template_name = 'employee/checklist_form.html'

    def get_object(self):
        employee = self.request.user.employee
        checklist,created = Checklist.objects.get_or_create(employee=employee)
        return checklist

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('users:dashboard')

def employee_registration(request):
    #user started employee registration path
    if request.method == 'GET':
        request.session["registration_path"] = "employee:create"
        return redirect("users:contact_information",pk=request.user.pk)


def get_positions(request):
    if request.method == 'GET':
        positions = list(Position.objects.values())
        return JsonResponse(positions,safe=False)

@permission_required("user.is_superuser")
def get_employees(request):
    if request.method == 'GET':
        position_id = request.GET.get("position_id")
        if position_id:
            employees = [
                    {
                        "email":employee.user.email,
                        "age": employee.user.age(),
                        "name": employee.user.get_full_name(),
                        "phone": employee.user.phone,
                        "is_lifeguard":employee.user.is_lifeguard,
                        "is_employee":employee.user.is_employee,
                    }
                    for employee in Employee.objects.filter(applied_positions__in=[position_id])]
            return JsonResponse(employees,safe=False)
        else:
            return JsonResponse({})


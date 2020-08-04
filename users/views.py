from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout,login,authenticate
from django.views.generic.edit import UpdateView,CreateView
from django.contrib.auth import views as auth_views

from .forms import CustomUserCreationForm
from .models import EmergencyContact,Address,User
from .forms import EmergencyContactForm,EmergencyContactFormSet


# Create your views here.
class DashboardView(TemplateView):
    template_name = 'users/dashboard.html'

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'

    def form_valid(self,form):
        valid = super().form_valid(form)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        new_user = authenticate(email=email,password=password)
        login(self.request,new_user)
        return valid

    def get_success_url(self):
        return reverse_lazy('users:dashboard')

class LogInView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('users:dashboard')

def logout_user(request):
    logout(request)
    return redirect('home')

class PasswordResetView(auth_views.PasswordResetView):
    template_name="users/password_reset_form.html"
    subject_template_name="users/password_reset_subject.txt"
    email_template_name="users/password_reset_email.html"

    def get_success_url(self):
        return reverse_lazy('users:password_reset_done')

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name="users/password_reset_confirm.html"

    def get_success_url(self):
        return reverse_lazy('users:password_reset_complete')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name="users/password_reset_done.html"

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name="users/password_reset_complete.html"

class ContactInformationUpdate(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name','phone','dob']
    template_name = 'users/contact_information_form.html'

    def get_success_url(self):
        return reverse_lazy('users:emergency_contact_create')

class EmergencyContactCreate(CreateView):
    model = EmergencyContact
    template_name = 'users/emergency_contact_form.html'
    form_class = EmergencyContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = EmergencyContactFormSet(queryset=EmergencyContact.objects.none())
        return context

    def post(self,request,*args,**kwargs):
        formset = EmergencyContactFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        return render(request,self.template_name,context={'formset':formset})

    def form_valid(self,formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = self.request.user
            instance.save()
        return super().form_valid(formset)

    def get_success_url(self):
        return reverse_lazy('users:address')

class EmergencyContactUpdate(UpdateView):
    model = EmergencyContact
    template_name = 'users/emergency_contact_form.html'
    form_class = EmergencyContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = EmergencyContactFormSet(queryset=EmergencyContact.objects.none())
        return context

    def post(self,request,*args,**kwargs):
        formset = EmergencyContactFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self,formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = self.request.user
            instance.save()
        return super().form_valid(formset)

    def get_success_url(self):
        return reverse_lazy('users:address')

class AddressCreate(CreateView):
    model = Address
    template_name = 'users/address_form.html'
    fields = ["street1","street2","city","state","zip"]

    def get_success_url(self):
        return reverse_lazy('lifeguard:create')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

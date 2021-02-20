from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.edit import UpdateView,CreateView
from django.contrib.auth import views as auth_views

from .models import EmergencyContact,Address,User
from .forms import (CustomUserCreationForm,
                    EmergencyContactForm,
                    EmergencyContactFormSet,
                    EmergencyContactInlineFormSet,
                    ContactInformationForm)



# Create your views here.
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'users/dashboard.html'

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'

    def form_valid(self,form):
        valid = super().form_valid(form)

        #log user in on sign up
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        new_user = log_user_in(self.request,email,password)

        #create address and
        assign_address_to_user(new_user,form.cleaned_data)

        return valid

    def get_success_url(self):
        return reverse_lazy('users:emergency_contact')

def log_user_in(request,email,password):
    new_user = authenticate(email=email,password=password)
    login(request,new_user)
    return new_user

def assign_address_to_user(user,cleaned_data):
    street1 = cleaned_data['street1']
    street2 = cleaned_data['street2']
    state = cleaned_data['state']
    city = cleaned_data['city']
    zip = cleaned_data['zip']
    Address.objects.create(
        user=user,
        street1=street1,
        street2=street2,
        city=city,
        state=state,
        zip=zip
    )

class LogInView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('users:dashboard')

def logout_user(request):
    logout(request)
    return redirect('users:login')

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

class ContactInformationUpdate(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ContactInformationForm
    template_name = 'users/contact_information_form.html'

    def get_success_url(self):
        return reverse_lazy('users:emergency_contact')

class EmergencyContactCreateOrUpdate(LoginRequiredMixin,UpdateView):
    model = EmergencyContact
    template_name = 'users/emergency_contact_form.html'
    form_class = EmergencyContactForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = {}
        formset = EmergencyContactInlineFormSet(instance=self.get_object())
        context['formset'] = formset
        return context

    def post(self,request,*args,**kwargs):
        formset = EmergencyContactInlineFormSet(request.POST,instance=self.get_object())
        if formset.is_valid():
            formset.save()
            return self.form_valid(formset)
        return render(request,self.template_name,context={'formset':formset})

    def get_success_url(self):
        return reverse_lazy('users:dashboard')

class AddressCreateOrUpdate(LoginRequiredMixin,UpdateView):
    model = Address
    template_name = 'users/address_form.html'
    fields = ["street1","street2","city","state","zip"]

    def get_object(self):
        obj,created = Address.objects.get_or_create(user=self.request.user)
        return obj

    def get_success_url(self):
        registration_path = self.request.session.get("registration_path")


        if registration_path:
            #user is either registering as a lifeguard or employee
            return reverse_lazy(registration_path)
        else:
            #user is updating their address
            return reverse_lazy('users:dashboard')


class AdminPanelView(PermissionRequiredMixin, View):
    template_name = "users/admin_panel.html"
    permission_required = "user.is_superuser"

    def get(self,request,*args,**kwargs):
        users = User.objects.all()
        return render(request,self.template_name,context={'users':users})


class AdminAddUserView(PermissionRequiredMixin,CreateView):
    permission_required = "user.is_superuser"
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/admin_add_user.html'

    def form_valid(self,form):
        valid = super().form_valid(form)
        form.save()

        email = form.cleaned_data['email']
        new_user = User.objects.get(email=email)

        #create address and
        assign_address_to_user(new_user,form.cleaned_data)
        return valid

    def get_success_url(self):
        return reverse_lazy('users:admin_panel')



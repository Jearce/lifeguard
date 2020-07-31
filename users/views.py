from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout,login,authenticate

from .forms import CustomUserCreationForm
from .models import User

# Create your views here.
class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    #success_url = reverse('dashboard')

    def form_valid(self,form):
        valid = super().form_valid(form)
        print(form.cleaned_data)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        new_user = authenticate(email=email,password=password)
        login(self.request,new_user)
        return valid

    def get_success_url(self):
        return reverse_lazy('dashboard')

class LogInView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')

class DashboardView(TemplateView):
    template_name = 'users/dashboard.html'

def logout_user(request):
    logout(request)
    return redirect('home')



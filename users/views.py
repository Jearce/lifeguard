from django.shortcuts import render
from django.urls import reverse,reverse_lazy
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm
from .models import User

# Create your views here.
class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = 'users/dashboard/'

class LogInView(LoginView):
    template_name = 'users/login.html'
    redirect_field_name = 'users/dashboard/'

class DashboardView(TemplateView):
    template_name = 'users/dashboard.html'

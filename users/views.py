from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm
from .models import User

# Create your views here.
class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'

class LogInView(LoginView):
    template_name = 'users/login.html'

from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from .forms import CustomUserCreationForm
from .models import User

# Create your views here.
class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('dashboard')

class LogInView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')

class DashboardView(TemplateView):
    template_name = 'users/dashboard.html'

def logout_user(request):
    logout(request)
    return redirect('home')



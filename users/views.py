from django.shortcuts import render
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from .models import User

# Create your views here.
class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'

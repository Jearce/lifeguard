from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from users.models import User

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class ContactInformationUpdate(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name','phone','dob']
    template_name = 'contact_information_form.html'

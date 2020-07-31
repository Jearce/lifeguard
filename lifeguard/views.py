from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView,CreateView
from django.urls import reverse_lazy

from users.models import User
from .models import EmergencyContact

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class ContactInformationUpdate(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name','phone','dob']
    template_name = 'lifeguard/contact_information_form.html'

    def get_success_url(self):
        return reverse_lazy('emergency_contact')

class EmergencyContactCreate(CreateView):
    model = EmergencyContact
    template_name = 'lifeguard/emergency_contact_form.html'
    success_url = 'lifeguard-registration/history/'
    fields = '__all__'




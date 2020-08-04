from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import UpdateView,CreateView
from django.urls import reverse_lazy

from users.models import User
from .models import EmergencyContact,Address,Lifeguard,Enroll,LifeguardClass
from .forms import EmergencyContactForm,EmergencyContactFormSet

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class ContactInformationUpdate(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name','phone','dob']
    template_name = 'lifeguard/contact_information_form.html'

    def get_success_url(self):
        return reverse_lazy('emergency_contact_create')

class EmergencyContactCreate(CreateView):
    model = EmergencyContact
    template_name = 'lifeguard/emergency_contact_form.html'
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
        return reverse_lazy('address')

class EmergencyContactUpdate(UpdateView):
    model = EmergencyContact
    template_name = 'lifeguard/emergency_contact_form.html'
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
        return reverse_lazy('address')



class EmergencyContactUpdate(CreateView):
    model = EmergencyContact
    template_name = 'lifeguard/emergency_contact_form.html'
    fields = ['name','relationship','phone']

    def get_success_url(self):
        return reverse_lazy('address')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class AddressCreate(CreateView):
    model = Address
    template_name = 'lifeguard/address_form.html'
    fields = ["street1","street2","city","state","zip"]

    def get_success_url(self):
        return reverse_lazy('lifeguard_create')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LifeguardCreate(CreateView):
    model = Lifeguard
    template_name = 'lifeguard/lifeguard_form.html'
    fields = [
        'already_certified',
        'wants_to_work_for_company',
        'payment_agreement',
        'payment_agreement_signature',
        'no_refunds_agreement',
        'electronic_signature'
    ]

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('classes')

class LifeguardClasses(View):
    def get(self,request,*args,**kwargs):
        classes = LifeguardClass.objects.all()
        return render(request,'lifeguard/classes.html',context={'classes':classes})

    def post(self,request,*args,**kwargs):
        lifeguard = Lifeguard.objects.get(user=request.user)
        lifeguard_class = LifeguardClass.objects.get(pk=self.kwargs['pk'])
        Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=lifeguard_class)
        return redirect('classes')






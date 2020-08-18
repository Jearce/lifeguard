from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import UpdateView,CreateView
from django.urls import reverse_lazy

from users.models import User
from .models import Lifeguard,Enroll,LifeguardClass
from .forms import LifeguardCertifiedForm,LifeguardForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class LifeguardCreateOrUpdate(UpdateView):
    model = Lifeguard
    template_name = 'lifeguard/lifeguard_form.html'
    form_class = LifeguardForm

    def get_object(self):
        try:
            obj = Lifeguard.objects.get(user=self.request.user)
        except Lifeguard.DoesNotExist:
            obj = Lifeguard(user=self.request.user)
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        user = self.request.user
        if user.lifeguard.already_certified:
            return reverse_lazy('lifeguard:already_certified')
        elif hasattr(user,'employee'):
            return reverse_lazy('lifeguard:classes')
        elif user.lifeguard.wants_to_work_for_company:
            return reverse_lazy('employee:create')
        return reverse_lazy('lifeguard:classes')

class LifeguardCertified(UpdateView):
    template_name = "lifeguard/already_certified_form.html"
    form_class = LifeguardCertifiedForm

    def get_object(self):
        return self.request.user.lifeguard

    def get_success_url(self):
        lifeguard = self.request.user.lifeguard
        if hasattr(lifeguard.user,'employee'):
            return reverse_lazy('lifeguard:classes')
        elif lifeguard.wants_to_work_for_company:
            return reverse_lazy('employee:create')
        return reverse_lazy('lifeguard:classes')

class LifeguardClasses(View):
    def get(self,request,*args,**kwargs):
        classes = LifeguardClass.objects.all()
        return render(request,'lifeguard/classes.html',context={'classes':classes})

    def post(self,request,*args,**kwargs):
        lifeguard = Lifeguard.objects.get(user=request.user)
        lifeguard_class = LifeguardClass.objects.get(pk=self.kwargs['pk'])
        Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=lifeguard_class)

        #TODO: redirect to payment view after successful enrollment
        return redirect('users:dashboard')

def lifeguard_registration(request):
    if request.method == 'GET':
        request.session["registration_path"] = "lifeguard:create"
        return redirect("users:contact_information",pk=request.user.pk)


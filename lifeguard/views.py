from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import UpdateView,CreateView
from django.urls import reverse_lazy

from users.models import User
from .models import Lifeguard,Enroll,LifeguardClass

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class LifeguardCreateOrUpdate(UpdateView):
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

    def get_object(self):
        print(self.request.user)
        try:
            obj = Lifeguard.objects.get(user=self.request.user)
        except Lifeguard.DoesNotExist:
            obj = Lifeguard(user=self.request.user)
        return obj

    #def form_valid(self,form):
    #    form.instance.user = self.request.user
    #    return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lifeguard:classes')

class LifeguardClasses(View):
    def get(self,request,*args,**kwargs):
        classes = LifeguardClass.objects.all()
        return render(request,'lifeguard/classes.html',context={'classes':classes})

    def post(self,request,*args,**kwargs):
        lifeguard = Lifeguard.objects.get(user=request.user)
        lifeguard_class = LifeguardClass.objects.get(pk=self.kwargs['pk'])
        Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=lifeguard_class)
        return redirect('lifeguard:classes')

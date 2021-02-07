from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import UpdateView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User,EmergencyContact
from lifeguard.models import Lifeguard,Enroll,LifeguardClass
from lifeguard.forms import LifeguardCertifiedForm,LifeguardForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class LifeguardCreateOrUpdate(LoginRequiredMixin,UpdateView):
    model = Lifeguard
    template_name = 'lifeguard/lifeguard_form.html'
    form_class = LifeguardForm

    def get(self,request,*args,**kwargs):
        user = self.request.user
        emergency_contacts = user.emergencycontact_set.all()
        if not emergency_contacts.exists():
            return redirect('users:emergency_contact')

        return super().get(request,*args,**kwargs)

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

        #if the user wants to work have them fill out the employee application if
        #they have not already done so
        elif user.lifeguard.wants_to_work_for_company and not user.is_employee:
            return reverse_lazy('employee:create')

        return reverse_lazy('lifeguard:classes')

class LifeguardCertified(LoginRequiredMixin,UpdateView):
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

class LifeguardClasses(LoginRequiredMixin,View):
    login_url= '/users/login/'

    def get(self,request,*args,**kwargs):
        user = self.request.user
        if user.is_lifeguard:
            lifeguard = user.lifeguard
            if not lifeguard.already_certified or lifeguard.certificate_expired():
                classes = LifeguardClass.objects.filter(lifeguard_certified_required=False,is_review=False)
            else:
                if lifeguard.certificate_expires_during_season():
                    classes = LifeguardClass.objects.filter(is_review=True)
                else:
                    classes = LifeguardClass.objects.filter(lifeguard_certified_required=True,is_review=lifeguard.needs_review())
        else:
            classes = LifeguardClass.objects.all()
         
        return render(request,'lifeguard/classes.html',context={'classes':classes.order_by('start_date')})

    def post(self,request,*args,**kwargs):

        user = self.request.user
        class_pk = self.kwargs['pk']
        if user.is_lifeguard:

            lifeguard_class = LifeguardClass.objects.get(pk=class_pk)
            Enroll.objects.create(
                lifeguard=user.lifeguard,
                lifeguard_class=lifeguard_class
            )

            return redirect("payment:enrollment_cart")

        else:
            return redirect("lifeguard:create")

class EnrolledClasses(LoginRequiredMixin,View):
    login_url= '/users/login/'

    def get(self, request,*args,**kwargs):
        user = self.request.user
        enrolled_classes = user.lifeguard.enroll_set.all()
        return render(
            request,'lifeguard/enrolled_classes.html',
            context={"enrolled_classes":enrolled_classes}
        )

def lifeguard_registration(request):
    if request.method == 'GET':
        request.session["registration_path"] = "lifeguard:create"
        return redirect("users:contact_information",pk=request.user.pk)

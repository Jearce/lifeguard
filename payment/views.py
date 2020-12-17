from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView
from django.views.generic.edit import FormView

import braintree

from payment.forms import LifeguardCheckoutForm
from payment.gateway import generate_client_token, transact, find_transaction


TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

class EnrollmentCart(View):
    def get(self, request, *args, **kwargs):
        lifeguard = self.request.user.lifeguard
        enrolled_classes = lifeguard.get_unpaid_lifeguard_classes()
        return render(request,'payment/enrollment_cart.html',context={"enrolled_classes":enrolled_classes})

    def post(self,request,*args,**kwargs):
        lifeguard = self.request.user.lifeguard
        enroll_pk=self.kwargs["pk"]
        lifeguard.enroll_set.get(pk=enroll_pk).delete()
        lifeguard.save()
        return redirect("payment:enrollment_cart")


class LifeguardCheckout(FormView):
    template_name = "payment/lifeguard_checkout.html"
    form_class = LifeguardCheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_token = generate_client_token()
        context["client_token"] = client_token
        return context

    def form_valid(self, form,**kwargs):
        lifeguard = self.request.user.lifeguard
        cost = sum(enroll.lifeguard_class.cost  for enroll in lifeguard.enroll_set.all())
        result = transact({
            "amount": cost,
            'payment_method_nonce':form.cleaned_data["nonce"],
            'options':{
                'submit_for_settlement':True,
                }
            })
        self.trasaction_id = result.transaction.id
        for enroll in lifeguard.enroll_set.all():
            enroll.paid = True
            enroll.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment:show_checkout', kwargs = {'transaction_id': self.trasaction_id})
        

def show_checkout(request,transaction_id):
    transaction = find_transaction(transaction_id)
    result = {"header":"Success","transaction":transaction}
    return render(request,"payment/show.html",context=result)

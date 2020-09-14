from django.shortcuts import render,redirect
from django.views.generic import View

import braintree

from payment.forms import PaymentForm
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
        return render(request,'payment/enrollment_cart.html')

# Create your views here.
def new_checkout(request):
    client_token = generate_client_token()
    form = PaymentForm()
    return render(request,'payment/new_checkout.html',context={'client_token':client_token,'form':form})

def create_checkout(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():

            lifeguard = request.user.lifeguard
            cost = sum(enroll.lifeguard_class.cost  for enroll in lifeguard.enroll_set.all())

            result = transact({
                "amount": cost,
                'payment_method_nonce':form.cleaned_data["nonce"],
                'options':{
                    'submit_for_settlement':True,
                }
            })

            return redirect("payment:show_checkout",transaction_id=result.transaction.id)

def show_checkout(request,transaction_id):
    transaction = find_transaction(transaction_id)
    result = {"header":"Success","transaction":transaction}
    return render(request,"payment/show.html",context=result)



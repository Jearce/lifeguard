from django.shortcuts import render

from payment.gateway import generate_client_token

# Create your views here.
def new_checkout(request):
    client_token = generate_client_token()
    return render(request,'payment/new_checkout.html',context={'client_token':client_token})


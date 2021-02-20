import json

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from payment.forms import LifeguardCheckoutForm

from square.client import Client

client = Client(
    square_version="2021-01-21",
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment="sandbox"
)


class EnrollmentCart(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        lifeguard = self.request.user.lifeguard
        enrolled_classes = lifeguard.get_unpaid_lifeguard_classes()
        return render(request, 'payment/enrollment_cart.html', context={"enrolled_classes": enrolled_classes})

    def post(self, request, *args, **kwargs):
        lifeguard = self.request.user.lifeguard
        enroll_pk = self.kwargs["pk"]
        lifeguard.enroll_set.get(pk=enroll_pk).delete()
        lifeguard.save()
        return redirect("payment:enrollment_cart")


class LifeguardCheckout(LoginRequiredMixin,FormView):
    template_name = "payment/lifeguard_checkout.html"
    form_class = LifeguardCheckoutForm

payment_api = client.payments

@csrf_exempt
def process_payment(request):
    lifeguard = request.user.lifeguard
    body = json.loads(request.body)
    cost = lifeguard.get_cost_for_enrolls()
    request_body = {
        "source_id": body["nonce"],
        "amount_money": {
            "amount": float(cost) * 100,
            "currency": "USD",
        },
        "location_id": body["location_id"],
        "idempotency_key": body["idempotency_key"]
    }
    response = payment_api.create_payment(request_body)
    if response.is_success():
        for enroll in lifeguard.get_unpaid_lifeguard_classes():
            enroll.paid = True
            enroll.save()
        return JsonResponse({"success": True, 'result': response.body})
    elif response.is_error():
        return JsonResponse({"success": False, 'result': response.errors})


def show_checkout(request, transaction_id):
    #transaction = find_transaction(transaction_id)
    result = {"header": "Success", "transaction": ""}
    return render(request, "payment/show.html", context=result)

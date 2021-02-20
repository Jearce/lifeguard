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

from users.models import Address

client = Client(
    square_version="2021-01-21",
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment="production"
)


class EnrollmentCart(LoginRequiredMixin, View):
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


class LifeguardCheckout(LoginRequiredMixin, FormView):
    template_name = "payment/lifeguard_checkout.html"
    form_class = LifeguardCheckoutForm


payment_api = client.payments
customer_api = client.customers


def create_customer(user, address):
    address_body = {
        key: value for key, value in address.items()
    }
    body = {
        "given_name": user.first_name,
        "family_name": user.last_name,
        "email_address": user.email,
        "phone_number": user.phone,
        "address": address_body
    }
    result = customer_api.create_customer(body)
    if result.is_success():
        return result.body
    else:
        return False


def search_customer(email):
    body = {
        "limit": 1,
        "query": {
            "filter": {
                "email_address": {
                    "exact": email
                }
            }
        }
    }

    result = customer_api.search_customers(body)
    if result.is_success():
        return result.body
    else:
        return False


@csrf_exempt
def process_payment(request):
    lifeguard = request.user.lifeguard
    body = json.loads(request.body)

    address = {
        key: value
        for key, value in body["customer_address"].items()
        if "default" not in key and "region" not in key
    }

    address["country"] = "US"

    s_results = search_customer(request.user.email)
    customer = None
    if s_results:
        customer = s_results["customers"][0]
    else:
        customer = create_customer(request.user, address)["customer"]

    cost = lifeguard.get_cost_for_enrolls()
    request_body = {
        "source_id": body["nonce"],
         "amount_money": {
             "amount": float(cost) * 100,
               "currency": "USD",
             },
        "location_id": body["location_id"],
           "idempotency_key": body["idempotency_key"],
           "customer_id": customer["id"]
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
    # transaction = find_transaction(transaction_id)
    result = {"header": "Success", "transaction": ""}
    return render(request, "payment/show.html", context=result)

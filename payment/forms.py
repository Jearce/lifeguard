from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field, Button, HTML


class LifeguardCheckoutForm(forms.Form):
    country = forms.CharField(max_length=255)
    region = forms.CharField(label="State", max_length=255)
    locality = forms.CharField(label="City", max_length=255)
    postal_code = forms.CharField(label="Zip", max_length=255)
    set_as_default = forms.BooleanField(
        label="Set as default billing address", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'lifeguard_payment_form'
        self.helper.layout = Layout(
            HTML("<h3 class='mb-3 mt-3'>Billing Address</h3>"),
            Div(
                'country',
                'region',
                'locality',
                'postal_code',
                'set_as_default',
            ),

            HTML("<h3 class='mb-3 mt-3'>Payment</h3>"),
            Div(
                HTML('''<div id="form-container">
			  <div id="sq-card-number"></div>
			  <div class="third" id="sq-expiration-date"></div>
			  <div class="third" id="sq-cvv"></div>
			  <div class="third" id="sq-postal-code"></div>
			  <button id="sq-creditcard" class="button-credit-card" onclick="onGetCardNonce(event)">submit payment</button>
                        </div>
                     ''')
            ),
        )

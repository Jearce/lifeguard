from django import forms

class PaymentForm(forms.Form):
    nonce = forms.CharField(
        max_length=1000,
        widget=forms.widgets.HiddenInput
    )


import json
import os

from django.conf import settings

import braintree


#if settings.DEBUG:
secrets_file = 'config.json'

with open(secrets_file) as f:
    SECRETS = json.loads(f.read())

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=SECRETS["BT_ENVIRONMENT"],
        merchant_id=SECRETS["BT_MERCHANT_ID"],
        public_key=SECRETS["BT_PUBLIC_KEY"],
        private_key=SECRETS["BT_PRIVATE_KEY"],
    )
)

def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)

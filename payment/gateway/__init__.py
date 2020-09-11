import json

from djagon.conf import settings

import braintree

if DEBUG:
    secrets_file = '../config.json'

with open(secrets_file) as f:
    SECRETS = json.loads(f)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=SECRETS["BT_ENVIRONMENT"],
        merchant_id=SECRETS["BT_MERCHANT_ID"],
        public_key=SECRETS["BT_PUBLIC_KEY"],
        private_key=SECRETS["BT_PRIVATE_KEY"],
    )
)

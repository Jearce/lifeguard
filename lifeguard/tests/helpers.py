from dateutil.relativedelta import relativedelta
from datetime import datetime

from lifeguard.models import Lifeguard


class LifeguardFactory:
    def __init__(
        self,
        user,
        already_certified=True,
        wants_to_work_for_company=True,
        payment_agreement=True,
        payment_agreement_signature=True,
        no_refunds_agreement=True,
        electronic_signature="Larry Smith",
        last_certified=None,
        certification=None
    ):
        self.user = user
        self.already_certified = already_certified
        self.wants_to_work_for_company = wants_to_work_for_company
        self.last_certified = last_certified
        self.payment_agreement = payment_agreement
        self.payment_agreement_signature = payment_agreement_signature
        self.no_refunds_agreement = no_refunds_agreement
        self.electronic_signature = electronic_signature
        self.certification = certification

    def create(self):
        lifeguard = Lifeguard.objects.create(
            user=self.user,
            already_certified=self.already_certified,
            wants_to_work_for_company=self.wants_to_work_for_company,
            payment_agreement=self.payment_agreement,
            payment_agreement_signature=self.payment_agreement_signature,
            no_refunds_agreement=self.no_refunds_agreement,
            electronic_signature=self.electronic_signature,
            last_certified=self.last_certified,
        )
        return lifeguard

def set_up_time(years,days):
    now = datetime.now()
    return now - relativedelta(years=years,days=days)

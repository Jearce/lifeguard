from datetime import datetime

from django.test import TestCase

from lifeguard.models import Lifeguard
from users.models import User

from dateutil.relativedelta import relativedelta

class LifeguardTest(TestCase):
    def setUp(self):
        self.password = 'secret!234'
        self.email = 'test@example.com'
        self.user = User.objects.create_user(password=self.password,email=self.email)

    def test_needs_a_review(self):
        needs_review_time = self.set_up_time(years=2,days=15)
        lifeguard = self.create_lifeguard(certified=True,last_certified=needs_review_time)
        self.assertTrue(lifeguard.needs_review())

    def test_does_not_need_review(self):
        no_review_time = self.set_up_time(years=2,days=30)
        lifeguard = self.create_lifeguard(certified=True,last_certified=no_review_time)
        self.assertFalse(lifeguard.needs_review())

    def test_certificate_is_expired(self):
        expired_time = self.set_up_time(years=2,days=30)
        lifeguard = self.create_lifeguard(certified=True,last_certified=expired_time)
        self.assertTrue(lifeguard.certificate_expired())

    def test_certificate_is_not_expired(self):
        still_valid_time = self.set_up_time(years=2,days=15)
        lifeguard = self.create_lifeguard(certified=True,last_certified=still_valid_time)
        self.assertFalse(lifeguard.certificate_expired())

    def create_lifeguard(self,certified,last_certified):
        lifeguard = Lifeguard.objects.create(
            user=self.user,
            already_certified=certified,
            wants_to_work_for_company=True,
            payment_agreement=True,
            payment_agreement_signature="Larry Smith",
            no_refunds_agreement=True,
            electronic_signature="Larry Smith",
            last_certified=last_certified,
        )
        return lifeguard

    def set_up_time(self,years,days):
        now = datetime.now()
        return now - relativedelta(years=years,days=days)

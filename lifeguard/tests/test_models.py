from django.test import TestCase

from lifeguard.models import Lifeguard
from users.models import User
from lifeguard.tests.helpers import set_up_time,LifeguardFactory

class LifeguardTest(TestCase):
    def setUp(self):
        self.password = 'secret!234'
        self.email = 'test@example.com'
        self.user = User.objects.create_user(password=self.password,email=self.email)
        self.factory = LifeguardFactory(user=self.user)

    def test_needs_a_review(self):
        needs_review_time = set_up_time(years=2,days=15)

        self.factory.last_certified = needs_review_time
        lifeguard = self.factory.create()

        self.assertTrue(lifeguard.needs_review())

    def test_does_not_need_review(self):
        no_review_time = set_up_time(years=2,days=30)

        self.factory.last_certified = no_review_time
        lifeguard = self.factory.create()

        self.assertFalse(lifeguard.needs_review())

    def test_certificate_is_expired(self):
        expired_time = set_up_time(years=2,days=30)

        self.factory.last_certified = expired_time
        lifeguard = self.factory.create()

        self.assertTrue(lifeguard.certificate_expired())

    def test_certificate_is_not_expired(self):
        still_valid_time = set_up_time(years=2,days=15)

        self.factory.last_certified = still_valid_time
        lifeguard = self.factory.create()

        self.assertFalse(lifeguard.certificate_expired())



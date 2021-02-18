from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.test import TestCase

from lifeguard.models import Lifeguard,Enroll,LifeguardClass
from users.models import User
from lifeguard.tests.helpers import set_up_time

from utils.test.helpers import LifeguardFactory

class LifeguardTest(TestCase):
    fixtures = ['classes.json']

    def setUp(self):
        self.password = 'secret!234'
        self.email = 'test@example.com'
        self.credentials = {
            'first_name':'Larry',
            'last_name':'John',
            'dob':'1995-06-09',
            'phone':'121 382 8292',
        }
        self.user = User.objects.create_user(password=self.password,email=self.email,**self.credentials)
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

    def test_certificate_expired_before_season(self):
        self.factory.last_certified = datetime(datetime.now().year,2,25) - relativedelta(years=2,days=30)
        lifeguard = self.factory.create()
        self.assertTrue(lifeguard.certificate_expired_before_season())

    def test_certificate_is_not_expired(self):
        still_valid_time = set_up_time(years=2,days=15)

        self.factory.last_certified = still_valid_time
        lifeguard = self.factory.create()

        self.assertFalse(lifeguard.certificate_expired())

    def test_user_is_lifeguard(self):
        lifeguard = self.factory.create()
        self.assertTrue(self.user.is_lifeguard)

    def test_lifeguard_employee_charged_correct_price(self):
        #lifeguard is/applied to employee position
        lifeguard = self.factory.create()
        lifeguard.user.is_employee = True
        lifeguard.user.save()

        #enrolls in a class
        first_class = LifeguardClass.objects.first()
        enroll = Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=first_class)
        lifeguard.enroll_set.add(enroll)
        lifeguard.save()

        #gets employee discount
        self.assertEqual(first_class.employee_cost,lifeguard.get_cost_for_enrolls())

    def test_lifeguard_charged_correct_price(self):
        lifeguard = self.factory.create()

        #enrolls in a class
        first_class = LifeguardClass.objects.first()
        enroll = Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=first_class)
        lifeguard.enroll_set.add(enroll)
        lifeguard.save()

        #gets employee discount
        self.assertEqual(first_class.cost,lifeguard.get_cost_for_enrolls())

    def test_charged_correct_price_for_many_enrolls(self):
        lifeguard = self.factory.create()

        #enrolls in classes
        first_class = LifeguardClass.objects.first()
        last_class = LifeguardClass.objects.last()
        enroll1 = Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=first_class)
        enroll2 = Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=last_class)
        lifeguard.enroll_set.add(enroll1,enroll2)
        lifeguard.save()

        #gets employee discount
        self.assertEqual(last_class.cost + first_class.cost,lifeguard.get_cost_for_enrolls())


    def test_certificate_expires_during_beginning_of_season(self):
        self.factory.last_certified = datetime(datetime.now().year,5,30) - relativedelta(years=2,days=30)
        lifeguard = self.factory.create()
        self.assertTrue(lifeguard.certificate_expires_during_season())
    

    def test_certificate_expires_during_end_of_season(self):
        self.factory.last_certified = datetime(datetime.now().year,6,30) - relativedelta(years=2,days=30)
        lifeguard = self.factory.create()
        self.assertTrue(lifeguard.certificate_expires_during_season())

    def test_get_unpaid_classes(self):
        lifeguard = self.factory.create()

        #enroll in some classes
        first_class = LifeguardClass.objects.first()
        last_class = LifeguardClass.objects.last()
        Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=first_class, paid=True)
        Enroll.objects.create(lifeguard=lifeguard,lifeguard_class=last_class)
        self.assertTrue(lifeguard.get_unpaid_lifeguard_classes().count() == 1)
        self.assertFalse(lifeguard.get_unpaid_lifeguard_classes().first().paid)

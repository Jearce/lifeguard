from django.urls import reverse
from django.test import TestCase

from payment import views

from lifeguard.models import LifeguardClass,Enroll

from utils.test import helpers

class EnrollmentCartTest(TestCase):
    fixtures = ['classes.json','positions.json','transportation.json']

    def setUp(self):
        super().setUp()
        self.user,self.email,self.password,_ = helpers.create_user()
        self.lifeguard = helpers.LifeguardFactory(user=self.user).create()
        login = self.client.login(email=self.email,password=self.password)

        #just two for now
        class1  = LifeguardClass.objects.first()
        class2  = LifeguardClass.objects.last()
        self.enrolls = [ Enroll.objects.create(lifeguard=self.lifeguard,lifeguard_class=lg_class)
            for lg_class in [class1, class2]
        ]

        self.lifeguard.enroll_set.add(*self.enrolls)
        self.lifeguard.save()


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('payment:enrollment_cart'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('payment:enrollment_cart'))
        self.assertTemplateUsed(response,'payment/enrollment_cart.html')

    def test_can_drop_enrollment(self):
        enroll = self.enrolls[0]
        self.assertEqual(self.lifeguard.enroll_set.count(),2)
        response = self.client.post(reverse('payment:drop_enrollment',kwargs={"pk":enroll.pk}))
        self.assertEqual(self.lifeguard.enroll_set.count(),1)
        self.assertEqual(response.status_code,302)

class LifeguardCheckout(TestCase):
    fixtures = ['classes.json','positions.json','transportation.json']

    def setUp(self):
        super().setUp()
        self.user,self.email,self.password,_ = helpers.create_user()
        self.lifeguard = helpers.LifeguardFactory(user=self.user).create()
        login = self.client.login(email=self.email,password=self.password)

        #just two for now
        class1  = LifeguardClass.objects.first()
        class2  = LifeguardClass.objects.last()
        enrolls = [ Enroll.objects.create(lifeguard=self.lifeguard,lifeguard_class=lg_class)
            for lg_class in [class1, class2]
        ]

        self.lifeguard.enroll_set.add(*enrolls)
        self.lifeguard.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('payment:lifeguard_checkout'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('payment:lifeguard_checkout'))
        self.assertTemplateUsed(response,'payment/lifeguard_checkout.html')

    def test_can_pay(self):
        response = self.client.get(reverse('payment:lifeguard_checkout'))
        self.assertEqual(response.status_code,302)



from datetime import datetime

from django.test import TestCase

from users.models import User
from employee.models import Employee,Position,Transportation


class EmployeeTest(TestCase):
    def setUp(self):
        self.position1 = Position.objects.create(title="Lifeguard",minimum_age=15,lifeguard_required=True)
        self.position2 = Position.objects.create(title="Supervisor",minimum_age=18,lifeguard_required=False)
        self.transportation = Transportation.objects.create(name="Car")
        self.user = User.objects.create_user(
            email="test@example.com",
            password="t3es3t123!",
            phone="713 383 8383",
            dob="1994-12-09",
        )
        self.employee = Employee.objects.create(
            user=self.user,
            who_referred_you="A friend",
            transportation=self.transportation,
            start_date=datetime.now(),
            end_date=datetime.now(),
            work_hours_desired=40,
            desired_pay_rate=18.5,
            pool_preference="Village Pool",
            subdivision="Village Subdivision",
            work_authorization=True,
            charged_or_arrested_resolved=False,
            charged_or_arrested_not_resolved=False,
            contract_employment_agreement=True,
            electronic_signature="Larry Berry",
            is_hired=True
        )

    def test_user_is_employee(self):
        self.employee.save()
        self.assertTrue(self.user.is_employee)

    def test_applied_for_non_lifeguard_position(self):
        self.employee.save()
        self.employee.applied_positions.set([self.position2])
        self.assertFalse(self.employee.applied_to_lifeguard_position())

    def test_applied_for_lifeguard_position(self):
        self.employee.save()
        self.employee.applied_positions.set([self.position1,self.position2])
        self.assertTrue(self.employee.applied_to_lifeguard_position())

from django.test import TestCase

from employee.models import Employee,Position,Transportation
from users.models import User

from utils.test.helpers import set_up_pdf_files_for_download

class CommonSetUp(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.email = 'test@example.com'
        cls.password = 'asdhf33!'
        cls.new_lifeguard = {
            "already_certified":False,#new lifeguard
            "wants_to_work_for_company":True,#should be redirected to employee register page
            "payment_agreement":True,
            "payment_agreement_signature":"Larry Johnson",
            "no_refunds_agreement":True,
            "electronic_signature":"Larry Johnson",
        }
        cls.employee_data = {
            "home_phone":"712 634 3328",
            "who_referred_you":"A friend.",
            "transportation":"1",
            "start_date":"2020-08-09",
            "end_date":"2020-12-10",
            "work_hours_desired":"40",
            "desired_pay_rate":"17.50",
            "pool_preference":"Village Pool",
            "subdivision":"My subdivision 122",
            "work_authorization":True,
            "charged_or_arrested_resolved":False,
            "charged_or_arrested_not_resolved":False,
            "contract_employment_agreement":True,
            "electronic_signature":"Larry Johnson",
        }

        cls.position1 = Position.objects.create(title="Lifeguard",minimum_age=15,lifeguard_required=True)
        cls.position2 = Position.objects.create(title="Supervisor",minimum_age=18,lifeguard_required=False)
        cls.transportation = Transportation.objects.create(name="Car",description="I will drive by car")

        #w4,i9,workers comp, and vaccination record
        cls.path_to_test_files = set_up_pdf_files_for_download()

    def setUp(self):
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            phone='832 188 2828',
            dob="1994-12-04",
        )
        self.client.login(email=self.email,password=self.password)

    def create_employee(self,applied_positions=None):
        if not applied_positions:
            #default position that requires lifeguard certificate
            applied_positions = [self.position1]

        employee = Employee(
            user=self.user,
            transportation=self.transportation,
            **{
                key:value
                for key, value in self.employee_data.items()
                if key != 'transportation' and key != 'applied_positions'}
        )
        employee.save()
        employee.applied_positions.set(applied_positions)
        return employee



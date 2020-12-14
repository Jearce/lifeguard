import os
from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site

from employee.models import PDFFile
from users.models import EmergencyContact,User
from lifeguard.models import Lifeguard

from dateutil.relativedelta import relativedelta


BASE_DIR = settings.BASE_DIR

class InlineFormsetManagmentFactory:
    def __init__(self,formset,extra,initial,min_num,max_num,records):
        '''
        records is a list of dictionaries

        '''
        self.formset = formset
        self.extra = extra
        self.initial = initial
        self.min_num = min_num
        self.max_num = max_num
        self.records = records

    def create_management_form(self):
        prefix = self.formset().prefix

        #management form
        mf = {}
        mf[f"{prefix}-TOTAL_FORMS"] = self.extra
        mf[f"{prefix}-INITIAL_FORMS"] = self.initial
        mf[f"{prefix}-MIN_NUM_FORMS"] = self.min_num
        mf[f"{prefix}-MAX_NUM_FORMS"] = self.max_num
        for i,record in enumerate(self.records):
            for key,value in record.items():
                mf[f"{prefix}-{i}-{key}"] = value
        return mf

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

def set_up_pdf_files_for_download():
    path_to_files = os.path.join(BASE_DIR,"functional_tests/files_used_to_test")
    PDFFile.objects.create(
        site=Site.objects.get_current(),
        w4=f"{path_to_files}/w4.pdf",
        i9=f"{path_to_files}/i9.pdf",
        workers_comp=f"{path_to_files}/workers_comp.pdf",
    )
    return path_to_files

def create_emergency_contact(user):
    emergency_contacts = [
        {
            "name":"Mary",
            "relationship":"mom",
            "phone":"712 434 2348"
        },
        {
            "name":"Jerry",
            "relationship":"dad",
            "phone":"712 434 2348"
        }
    ]

    user_ems = [
        EmergencyContact.objects.create(user=user,**em)
        for em in emergency_contacts
    ]
    return user_ems

def create_user():
    '''Creates user and returns user,email,password, and credentials as tuple'''

    email='test@example.com'
    password='2dhd7!42'
    credentials = {
        'first_name':'Larry',
        'last_name':'John',
        'dob':'1995-06-09',
        'phone':'121 382 8292',
    }
    user = User.objects.create_user(
        email=email,
        password=password,
        **credentials
    )
    return user,email,password,credentials

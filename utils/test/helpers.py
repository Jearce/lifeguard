import os

from django.conf import settings
from django.contrib.sites.models import Site

from employee.models import PDFFile

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

def set_up_pdf_files_for_download():
    path_to_files = os.path.join(BASE_DIR,"functional_tests/files_used_to_test")
    PDFFile.objects.create(
        site=Site.objects.get_current(),
        w4=f"{path_to_files}/w4.pdf",
        i9=f"{path_to_files}/i9.pdf",
        workers_comp=f"{path_to_files}/workers_comp.pdf",
    )




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



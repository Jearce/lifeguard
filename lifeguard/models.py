from datetime import datetime

from django.db import models
from django.db.models import Sum
from users.models import User

from dateutil.relativedelta import relativedelta

# Create your models here.
class Lifeguard(models.Model):
    WORK_CHOICES = [
        (True,"Yes (I want the discounted employee rate)"),
        (False,"No, I will be working elsewhere (NOT eligible for discount)"),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    already_certified = models.BooleanField("Are you a certified lifeguard?",choices=[(True,"Yes"),(False,"No")],default=None)
    wants_to_work_for_company = models.BooleanField("Do you plan to work for Gulf Coast Aquatics?",choices=WORK_CHOICES,default=None)
    payment_agreement = models.BooleanField()
    payment_agreement_signature = models.CharField(max_length=255)
    no_refunds_agreement = models.BooleanField()
    electronic_signature = models.CharField("Electronic signature",max_length=255)
    last_certified = models.DateField(blank=False,null=True)
    certification = models.FileField(blank=False,null=True)
    online_portion_complete = models.BooleanField(default=False)

    def get_unpaid_lifeguard_classes(self):
        return self.enroll_set.filter(paid=False)

    def get_cost_for_enrolls(self):
        enrolled_class = LifeguardClass.objects.filter(students=self,enroll__paid=False)
        if  self.user.is_employee:
            return enrolled_class.aggregate(Sum("employee_cost")).get("employee_cost__sum")
        else:
            return enrolled_class.aggregate(Sum("cost")).get("cost__sum")


    def certificate_expired(self):
        date_from_being_certified = self.get_last_certified() + self.get_experience()
        return date_from_being_certified > self.get_experiation_date_of_certificate()

    def needs_review(self):
        experience = self.get_experience()
        return experience.years == 2 and experience.days < 30

    def get_experiation_date_of_certificate(self):
        #certifcate is valid for 2 years and 30 days of being certified
        duration_of_certificate = relativedelta(years=2,days=30)
        return self.date_certified + duration_of_certificate

    def get_experience(self):
        now = datetime.now()
        diff = relativedelta(now,self.date_certified)
        return diff

    @property
    def date_certified(self):
        date_certified = self.get_last_certified()
        return date_certified

    def get_last_certified(self):
        if self.last_certified:
            return datetime(self.last_certified.year,self.last_certified.month,self.last_certified.day)
        else:
            return datetime.now()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def save(self,*args,**kwargs):
        self.user.is_lifeguard = True
        self.user.save()
        super().save(*args,**kwargs)

class LifeguardClass(models.Model):
    course = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    employee_cost = models.DecimalField(max_digits=6, decimal_places=2)
    students = models.ManyToManyField(Lifeguard,through="Enroll")
    lifeguard_certified_required = models.BooleanField(
        "Do the students need to be lifeguard certified to take this class?",
        choices=[(True, "Yes"),(False,"No")],
        default=False,
    )
    is_review = models.BooleanField(
        "Is this class a review for expiring lifeguard certificates?",
        choices=[(True, "Yes"),(False,"No")],
        default=False,
    )

    def __str__(self):
        return self.course


class LifeguardClassSession(models.Model):
    lifeguard_class = models.ForeignKey(LifeguardClass, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "Class session for %s" %self.lifeguard_class

    

class Enroll(models.Model):
    lifeguard = models.ForeignKey(Lifeguard,on_delete=models.CASCADE)
    lifeguard_class = models.ForeignKey(LifeguardClass,on_delete=models.CASCADE)
    grade = models.PositiveIntegerField(blank=True,null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "Enrollment for {} in {}".format(self.lifeguard.user.first_name,self.lifeguard_class.course)

from datetime import datetime, timedelta

from django.db import models
from django.db.models import Sum
from django.conf import settings
from users.models import User

from storage_backends import PublicMediaStorage, PrivateMediaStorage

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
    certification = models.FileField(storage=PrivateMediaStorage() if settings.USE_S3 else None,blank=False,null=True)
    online_portion_complete = models.BooleanField(default=False)
    online_record = models.FileField(blank=True, null=True)


    @property
    def date_certified(self):
        return self.get_last_certified()

    @property
    def date_certificate_expires(self):
        #expires at 2 years and 30 days -> 760 days
        return self.get_last_certified() + timedelta(days=760) 


    def get_unpaid_lifeguard_classes(self):
        return self.enroll_set.filter(paid=False)


    def get_cost_for_enrolls(self):
        enrolled_class = LifeguardClass.objects.filter(students=self,enroll__paid=False)
        if  self.user.is_employee:
            return enrolled_class.aggregate(Sum("employee_cost")).get("employee_cost__sum")
        else:
            return enrolled_class.aggregate(Sum("cost")).get("cost__sum")


    def certificate_expired_before_season(self):
        return self.date_certificate_expires < datetime(datetime.now().year,3,1)

    def certificate_expired(self):
        return self.date_certificate_expires < datetime.now()



    def certificate_expires_during_season(self):
        now = datetime.now()
        start_of_march = datetime(now.year,3,1)
        end_of_july = datetime(now.year,7,30)
        return (self.date_certificate_expires >= start_of_march) and (self.date_certificate_expires <= end_of_july)


    def needs_review(self):
        experience = self.get_experience()
        return experience.years == 2 and experience.days < 30


    def get_experience(self):
        return relativedelta(datetime.now(),self.date_certified)


    def get_last_certified(self):
        if self.last_certified:
            return datetime(self.last_certified.year,self.last_certified.month,self.last_certified.day)
        else:
            return datetime.now()


    def save(self,*args,**kwargs):
        self.user.is_lifeguard = True
        self.user.save()
        super().save(*args,**kwargs)


    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class LifeguardClass(models.Model):

    class Meta:
        verbose_name = "Session"

    course = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    employee_cost = models.DecimalField(max_digits=6, decimal_places=2)
    students = models.ManyToManyField(Lifeguard,through="Enroll")
    lifeguard_certified_required = models.BooleanField(
        "Do the students need to be lifeguard certified to take this class?",
        choices=[(True, "Yes"),(False,"No")],
        default=False,
    )
    max_enrollment = models.PositiveIntegerField(default=20)
    min_enrollment = models.PositiveIntegerField(default=10)
    is_available = models.BooleanField(default=True)

    is_review = models.BooleanField(
        "Is this class a review?",
        choices=[(True, "Yes"),(False,"No")],
        default=False,
    )
    is_refresher = models.BooleanField(
        "Is this class a refresher?",
        choices=[(True, "Yes"),(False,"No")],
        default=False,
    )
    refresher_url = models.CharField(max_length=255,null=True,blank=True)


    def get_sessions(self):
        return self.lifeguardclasssession_set.all().order_by("date")


    def meets_min_enrollment(self):
        return self.enroll_set.count() >= self.min_enrollment


    def exceeds_max_enrollment(self):
        return self.enroll_set.count() >= self.max_enrollment


    def __str__(self):
        return self.course


class LifeguardClassSession(models.Model):

    class Meta:
        verbose_name = "Session date"

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
    brick = models.BooleanField("Passed brick test",blank=True, null=True)
    tread = models.BooleanField("Can tread for 2 minutes",blank=True, null=True)
    swim_300 = models.BooleanField("Can swim 300 meters",blank=True, null=True)

    def __str__(self):
        return "Enrollment for {} in {}".format(self.lifeguard.user.first_name,self.lifeguard_class.course)

from django.db import models
from django.utils import timezone
from django.contrib.sites.models import Site

from users.models import User

# Create your models here.

BOOLEAN_CHOICES = [(True,"Yes"),(False,"No")]

class Transportation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=255)
    minimum_age = models.PositiveIntegerField(
        "Minimum age requirement",
        default=15
    )
    lifeguard_required = models.BooleanField(
        "Is lifeguard certification required for this position?",
        choices=BOOLEAN_CHOICES,
        default=True
    )

    def __str__(self):
        return f"{self.title} (Must be at least {self.minimum_age} years old)"

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    home_phone = models.CharField(max_length=12,blank=True,null=True)
    who_referred_you = models.CharField("Who referred you to us?",max_length=255)
    transportation = models.ForeignKey(
        "Transportation",
        on_delete=models.CASCADE
    )
    applied_positions = models.ManyToManyField(Position)
    start_date = models.DateField()
    end_date = models.DateField()
    work_hours_desired = models.PositiveIntegerField()
    desired_pay_rate = models.DecimalField(
        "Asking rate of pay",
        max_digits=6,
        decimal_places=2
    )
    pool_preference = models.CharField(max_length=255)
    subdivision = models.CharField(
        "Which subdivision do you live in or nearby",
        max_length=255
    )

    work_authorization = models.BooleanField(choices=BOOLEAN_CHOICES,blank=False,default=None)
    charged_or_arrested_resolved = models.BooleanField(choices=BOOLEAN_CHOICES,blank=False,default=None)
    charged_or_arrested_not_resolved = models.BooleanField(choices=BOOLEAN_CHOICES,blank=False,default=None)
    contract_employment_agreement = models.BooleanField()
    electronic_signature = models.CharField("Your name",max_length=255)
    is_hired = models.BooleanField("hire",choices=BOOLEAN_CHOICES,blank=True,null=True)
    application_under_review = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def applied_to_lifeguard_position(self):
        return any(position.lifeguard_required for position in self.applied_positions.all())

    def save(self, *args, **kwargs):
        self.user.is_employee = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

class EmployeeEducation(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    school_name = models.CharField(
        "Name of school",
        max_length=255
    )
    grade_year = models.CharField(
        "What grade/year are you",
        max_length=255
    )
    attending_college =  models.BooleanField(
        "Will you attend college this fall?",
        choices=BOOLEAN_CHOICES,
        blank=True,
        null=True,
    )
    date_leaving_to_college = models.DateField(
        "If leaving to college in the Fall when will you leave?",
        blank=True,
        null=True,
    )

class JobHistory(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    previous_employer = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField("Starting date of employement")
    end_date = models.DateField("Ending date of employement?")
    reason_for_leaving = models.TextField()

class Checklist(models.Model):
    ACCOUNT_TYPES = [('S',"Savings Account"),("C","Checkings Account")]

    employee = models.OneToOneField(Employee,on_delete=models.CASCADE)
    photo_id = models.FileField("Photo Identification",null=True, blank=True)
    social_security_card = models.FileField(null=True, blank=True)
    social_security_number = models.CharField(null=True, blank=True, max_length=10)
    birth_certificate = models.FileField(blank=True,null=True)
    w4 = models.FileField(null=True, blank=True)
    i9 = models.FileField(null=True, blank=True)
    workers_comp = models.FileField(null=True, blank=True)
    vaccination_record = models.FileField(blank=True,null=True)
    hepB_waiver_signature = models.CharField(blank=True,null=True,max_length=255)
    banking_name = models.CharField(null=True,blank=True, max_length=255)
    account_type = models.CharField(choices=ACCOUNT_TYPES,max_length=1,null=True, blank=True, default=None)
    account_number = models.CharField(null=True,blank=True,max_length=255)
    router_number = models.CharField(null=True,blank=True,max_length=255)
    email_address = models.EmailField(null=True,blank=True,max_length=255)
    auth_signature = models.CharField(null=True,blank=True,max_length=255)
    awknowledgement_form_signature = models.CharField(null=True, blank=True,max_length=255)
    date = models.DateField(default=timezone.now)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return "Checklist for" +" "+ self.employee.user.get_full_name()

class PDFFile(models.Model):
    site = models.OneToOneField(Site,on_delete=models.CASCADE)
    w4 = models.FileField(blank=True, null=True)
    i9 = models.FileField(blank=True, null=True)
    workers_comp = models.FileField(blank=True, null=True)
    employee_handbook = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"PDF files for {self.site.name}"



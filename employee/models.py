from django.db import models
from users.models import User

# Create your models here.
class Transportation(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

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
        choices=[(True,"Yes"),(False,"No")],
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

    start_date = models.DateField("Date available to start")
    end_date = models.DateField(
        "Ending date - This is not official. A notice is still required."
    )

    work_hours_desired = models.PositiveIntegerField(
        "Number of hours desired per week"
    )
    desired_pay_rate = models.DecimalField(
        "Asking rate of pay",
        max_digits=6,
        decimal_places=2
    )
    pool_preference = models.CharField("Pool preference",max_length=255,default="")
    subdivision = models.CharField(
        "Which subdivision do you live in or nearby",
        max_length=255
    )

    BOOLEAN_CHOICES = [(True,"Yes"),(False,"No")]
    work_authorization = models.BooleanField('',choices=BOOLEAN_CHOICES,blank=False,default=None)
    charged_or_arrested = models.BooleanField('',choices=BOOLEAN_CHOICES,blank=False,default=None)
    has_felony = models.BooleanField('',choices=BOOLEAN_CHOICES,blank=False,default=None)
    contract_employment_agreement = models.BooleanField("I agree")
    electronic_signature = models.CharField("Your name",max_length=255)
    is_hired = models.BooleanField("Accepted for hire",choices=BOOLEAN_CHOICES,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.user.is_employee = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email


class EmployeeEducation(models.Model):
    CHOOICES = [(True,"Yes"),(False,"No")]
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
        choices=CHOOICES,
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



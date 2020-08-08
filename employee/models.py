from django.db import models
from users.models import User

# Create your models here.
class Transportation(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    home_phone = models.CharField(max_length=12)
    start_date = models.DateField()
    end_date = models.DateField()
    who_referred_you = models.TextField("Who referred you to us?")
    transpotation = models.ForeignKey(Transportation,on_delete=models.CASCADE)
    CHOICES = [('L','Lifeguard'),('S','Supervisor'),('M','Manager')]
    applied_position = models.CharField(CHOICES,max_length=1)
    work_hours_desired = models.PositiveIntegerField()
    desired_pay_rate = models.DecimalField(max_digits=6, decimal_places=2)
    work_authorization = models.CharField(max_length=255)
    charged_or_arrested = models.BooleanField()
    has_felony = models.BooleanField()
    contract_employment_agreement = models.CharField(max_length=255)
    electronic_signature = models.CharField("Your name",max_length=255)
    subdivision = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

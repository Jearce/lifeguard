from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

from dateutil.relativedelta import relativedelta

# Create your models here.
class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField('email address',unique=True)
    phone = models.CharField('phone number',max_length=16)
    dob = models.DateField('date of birth',max_length=8)
    is_employee = models.BooleanField(default=False)
    is_lifeguard = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','phone','dob']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def age(self):
        dob = datetime(self.dob.year,self.dob.month,self.dob.day)
        now = datetime.now()
        diff =  relativedelta(now,dob)
        return diff.years

    def get_full_name(self):
        return self.first_name + " " + self.last_name

class EmergencyContact(models.Model):
    name = models.CharField('name',max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    relationship = models.CharField('relationship',max_length=255)
    phone = models.CharField('phone',max_length=255)

    def __str__(self):
        return self.name

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255,blank=True,null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

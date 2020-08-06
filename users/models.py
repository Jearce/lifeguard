from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField('email address',unique=True)
    phone = models.CharField('phone number',max_length=16,blank=True,null=True)
    dob = models.DateField('date of birth',max_length=8,blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

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

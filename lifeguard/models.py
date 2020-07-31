from django.db import models
from users.models import User

# Create your models here.
class EmergencyContact(models.Model):
    name = models.CharField('name',max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    relationship = models.CharField('relationship',max_length=255)
    phone = models.CharField('phone',max_length=255)

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255,blank=True,null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

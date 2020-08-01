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

class Lifeguard(models.Model):
    WORK_CHOICES = [
        ('Y',"Yes (I want the discounted employee rate)"),
        ('N',"I will be working elsewhere (NOT eligible for discount)"),
        ("O","Other")
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    already_certified = models.BooleanField("Are you a certified lifeguard?",choices=[("Y","Yes"),("N","No")])
    wants_to_work_for_company = models.CharField("Do you plan to work for Gulf Coast Aquatics?",choices=WORK_CHOICES,max_length=1)
    payment_agreement = models.BooleanField("I agree")
    payment_agreement_signature = models.CharField("Your name",max_length=255)
    no_refunds_agreement = models.BooleanField("I agree")
    electronic_signature = models.CharField("Electronic signature",max_length=255)
    last_certified = models.DateField(blank=True,null=True)
    certification = models.ImageField(blank=True,null=True)
    online_portion_complete = models.BooleanField(default=True)





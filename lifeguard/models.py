from django.db import models
from users.models import User

# Create your models here.
class Lifeguard(models.Model):
    WORK_CHOICES = [
        ('Y',"Yes (I want the discounted employee rate)"),
        ('N',"I will be working elsewhere (NOT eligible for discount)"),
        ("O","Other")
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    already_certified = models.CharField("Are you a certified lifeguard?",choices=[("Y","Yes"),("N","No")],max_length=1)
    wants_to_work_for_company = models.CharField("Do you plan to work for Gulf Coast Aquatics?",choices=WORK_CHOICES,max_length=1)
    payment_agreement = models.BooleanField("I understand and agree")
    payment_agreement_signature = models.CharField("Your name",max_length=255)
    no_refunds_agreement = models.BooleanField("I agree")
    electronic_signature = models.CharField("Electronic signature",max_length=255)
    last_certified = models.DateField(blank=True,null=True)
    certification = models.ImageField(blank=True,null=True)
    online_portion_complete = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class LifeguardClass(models.Model):
    course = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    employee_cost = models.DecimalField(max_digits=6, decimal_places=2)
    students = models.ManyToManyField(Lifeguard,through="Enroll")

    def __str__(self):
        return self.course

class Enroll(models.Model):
    lifeguard = models.ForeignKey(Lifeguard,on_delete=models.CASCADE)
    lifeguard_class = models.ForeignKey(LifeguardClass,on_delete=models.CASCADE)
    grade = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        return "Enrollment for {} in {}".format(self.lifeguard.user.first_name,self.lifeguard_class.course)

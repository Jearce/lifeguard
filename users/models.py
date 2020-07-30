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


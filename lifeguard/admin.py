from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Lifeguard)
admin.site.register(models.LifeguardClass)
admin.site.register(models.Enroll)
admin.site.register(models.EmergencyContact)
admin.site.register(models.Address)



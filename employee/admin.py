from django.contrib import admin
from employee import models

# Register your models here.
admin.site.register(models.Employee)
admin.site.register(models.Transportation)
admin.site.register(models.Position)
admin.site.register(models.Checklist)
admin.site.register(models.EmployeeFile)

from django.contrib import admin
from employee import models

# Register your models here.
@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self,db_field,request,**kwargs):
        if db_field.name == 'applied_positions':
            kwargs["queryset"] = models.Position.objects.filter(employee=request.user.employee)
        return super().formfield_for_manytomany(db_field,request,**kwargs)

admin.site.register(models.Transportation)
admin.site.register(models.Position)
admin.site.register(models.Checklist)
admin.site.register(models.PDFFile)

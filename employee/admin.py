from django.contrib import admin
from django.db.models.query import RawQuerySet
from django.urls import reverse
from django.utils.html import format_html

from employee import models

class ChecklistFilter(admin.SimpleListFilter):
    title = ('check list that are complete')
    parameter_name = 'checklist'

    def lookups(self,request,model_admin):
        return (
            ("complete","completed check list"),
            ("not","have not completed check list")
        )

    def queryset(self,request,queryset):
        if self.value == "complete":
            return queryset.filter(checklist__isnull=False)
        if self.value() == "not":
            return queryset.filter(checklist__isnull=True)


# Register your models here.
@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'created_on',
        'check_list'
    )

    list_filter = (
        ChecklistFilter,
    )

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field=from_field)
        request.employee = obj
        return obj

    def formfield_for_manytomany(self,db_field,request,**kwargs):
        if db_field.name == 'applied_positions' and hasattr(request,'employee'):
            print("yes")
            kwargs["queryset"] = models.Position.objects.filter(employee=request.employee)
        return super().formfield_for_manytomany(db_field,request,**kwargs)

    def delete_queryset(self,request,queryset):
        for e in queryset:
            e.user.is_employee = False
            e.user.save()
        return super().delete_queryset(request,queryset)

    def check_list(self,obj):
        url = reverse('admin:employee_checklist_change',args=(obj.checklist.pk,))
        return format_html("<a href='{url}'>checklist</a>",url=url)



admin.site.register(models.Transportation)
admin.site.register(models.Position)
admin.site.register(models.Checklist)
admin.site.register(models.PDFFile)

from django.contrib import admin
from lifeguard import models

from dateutil.relativedelta import relativedelta

# Register your models here.
@admin.register(models.Lifeguard)
class LifeguardAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'class_needed',
        'years_since_last_certified'
    )

    def class_needed(self,obj):
        exper = obj.get_experience().years
        if obj.needs_review():
            return "needs review"
        elif obj.get_experience().years >= 1 and obj.user.is_employee:
            return "needs refresher"
        elif exper == 0 and not obj.already_certified:
            return "certificate class"

    def delete_queryset(self,request,queryset):
        for e in queryset:
            e.user.is_lifeguard = False
            e.user.save()
        return super().delete_queryset(request,queryset)

    def years_since_last_certified(self, obj):
        if obj.already_certified:
            return obj.get_experience().years



admin.site.register(models.LifeguardClass)
admin.site.register(models.Enroll)

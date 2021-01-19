from django.contrib import admin
from django import forms
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

    def class_needed(self, obj):
        exper = obj.get_experience().years
        if obj.needs_review():
            return "needs review"
        elif obj.get_experience().years >= 1 and obj.user.is_employee:
            return "needs refresher"
        elif exper == 0 and not obj.already_certified:
            return "certificate class"

    def delete_queryset(self, request, queryset):
        for e in queryset:
            e.user.is_lifeguard = False
            e.user.save()
        return super().delete_queryset(request, queryset)

    def years_since_last_certified(self, obj):
        if obj.already_certified:
            return obj.get_experience().years


class LifeguardClassSessionForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = models.LifeguardClassSession

    def clean(self):
        start_date = self.cleaned_data.get('start_time')
        end_date = self.cleaned_data.get('end_time')
        if start_date > end_date:
            raise forms.ValidationError("Start time must be before end time")
        return self.cleaned_data


@admin.register(models.LifeguardClassSession)
class LifeguardClassSessionAdmin(admin.ModelAdmin):
    form = LifeguardClassSessionForm
    list_display = ('lifeguard_class','date', 'start_time', 'end_time',)
    list_filter = ('lifeguard_class',)


@admin.register(models.Enroll)
class EnrollAdmin(admin.ModelAdmin):
    list_display = ('lifeguard','lifeguard_class', 'paid', 'grade')
    list_filter = ('lifeguard_class', 'paid',)

    search_fields = ('lifeguard__user__first_name','lifeguard__user__last_name')



admin.site.register(models.LifeguardClass)

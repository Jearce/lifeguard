from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html


from lifeguard import models


from dateutil.relativedelta import relativedelta


@admin.register(models.Lifeguard)
class LifeguardAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'class_needed',
        'already_certified',
        'date_certificate_expires',
        'wants_to_work',
        'employee_application'
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

    def date_cerificate_expires(self, obj):
        if obj.already_certified:
            return obj.date_certifcate_expires

    def wants_to_work(self, obj):
        return "Yes" if obj.wants_to_work_for_company else "No"

    def employee_application(self,obj):
        if obj.wants_to_work_for_company and obj.user.is_employee:
            url =  reverse('admin:employee_employee_change',args=(obj.user.employee.pk,))
            return format_html("<a href='{url}'>application</a>",url=url)


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
    list_display = (
        'lifeguard',
        'lifeguard_class',
        'paid',
        'grade',
        'brick',
        'tread',
        'swim_300',
        )

    list_filter = (
        'lifeguard_class',
         'paid',
         'brick',
         'tread',
         'swim_300'
         )

    search_fields = ('lifeguard__user__first_name','lifeguard__user__last_name')



admin.site.register(models.LifeguardClass)

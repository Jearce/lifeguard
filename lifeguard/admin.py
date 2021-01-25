from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html

from lifeguard import models

class LifeguardClassFilter(admin.SimpleListFilter):
    title = ('lifeguard class')
    parameter_name = "class needed"

    def lookups(self,request,model_admin):
        return (
            ('review',"needs review"),
            ('refresher',"needs refresher"),
            ('lifeguard',"needs lifeguard class"),
        )

    def queryset(self,request,queryset):
        if self.value() == "review":
            return queryset.filter(id__in=[ obj.id for obj in queryset if obj.needs_review()])
        if self.value() == "refresher":
            return queryset.filter(id__in=[obj.id for obj in queryset if (obj.get_experience().days > 1 or obj.get_experience().years >= 1) and obj.user.is_employee])
        if self.value() == "lifeguard":
            return queryset.filter(id__in=[obj.id for obj in queryset if obj.certificate_expired() or not obj.already_certified])



@admin.register(models.Lifeguard)
class LifeguardAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'user',
        'class_needed',
        'already_certified',
        'certificate_expires_on',
        'wants_to_work',
        'employee_application'
    )

    search_fields = ('user__email','user__phone','user__first_name','user__last_name')

    list_filter = (LifeguardClassFilter,)


    def class_needed(self, obj):
        if obj.needs_review():
            return "needs review"
        elif obj.certificate_expired() or not obj.already_certified:
            return "certificate class"
        elif obj.user.is_employee:
            return "needs refresher"


    def delete_queryset(self, request, queryset):
        for e in queryset:
            e.user.is_lifeguard = False
            e.user.save()
        return super().delete_queryset(request, queryset)


    def certificate_expires_on(self, obj):
        if obj.already_certified:
            return obj.date_certificate_expires


    def first_name(self,obj):
        return obj.user.first_name


    def last_name(self,obj):
        return obj.user.last_name


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


class LifeguardClassForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = models.LifeguardClass

    def clean(self):
        is_refresher = self.cleaned_data.get('is_refresher')
        refresher_url = self.cleaned_data.get('refresher_url')
        if is_refresher and not refresher_url :
            raise forms.ValidationError("Refresher class must have a refresher url")
        return self.cleaned_data


@admin.register(models.LifeguardClass)
class LifeguardClassAdmin(admin.ModelAdmin):
    form = LifeguardClassForm



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
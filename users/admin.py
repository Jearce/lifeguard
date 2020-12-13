from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

import  datetime
from dateutil.relativedelta import relativedelta

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User,EmergencyContact,Address

class LifeguardListFilter(admin.SimpleListFilter):
    title = ("applied as a lifeguard")
    parameter_name = "lifeguard"

    def lookups(self,request,model_admin):
        return (
            ("complete","completed lifeguard application"),
            ("not","did not complete lifeguard application"),
        )

    def queryset(self,request,queryset):
        if self.value() == "completed":
            return queryset.filter(lifeguard__isnull=False)
        if self.value() == "not":
            return queryset.filter(lifeguard__isnull=True)

class EmployeeListFilter(admin.SimpleListFilter):
    title = ("applied as a employee")
    parameter_name = "employee"

    def lookups(self,request,model_admin):
        return (
            ("complete","completed employee application"),
            ("not","did not complete employee application"),
        )

    def queryset(self,request,queryset):
        if self.value() == "completed":
            return queryset.filter(employee__isnull=False)
        if self.value() == "not":
            return queryset.filter(employee__isnull=True)

class AgeListFilter(admin.SimpleListFilter):
    title = ('age')
    parameter_name = "age"

    def lookups(self,request,model_admin):
        return (
            ('>=18',"18 years or older"),
            ('18&15',"Between 15 and 18 years old"),
            ('15',"15 years old"),
            ("<15","Younger than 15 years old"),
        )

    def queryset(self,request,queryset):
        age_15 = (datetime.date.today() - relativedelta(years=15)).year
        age_18 = (datetime.date.today() - relativedelta(years=18)).year

        if self.value() == ">=18":
            return queryset.filter(dob__year__lt=age_18)

        if self.value() == "18&15":
            return queryset.filter(dob__year__range=[age_18,age_15])

        if self.value() == "15":
            return queryset.filter(dob__year=age_15)

        if self.value() == "<15":
            return queryset.filter(dob__year__gt=age_15)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
        'age',
        'phone',
        'employee_application',
        'lifeguard_application',
    )

    list_filter = (
        'employee__is_hired',
        'lifeguard__already_certified',
        AgeListFilter,
        LifeguardListFilter,
        EmployeeListFilter,

    )

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name','phone','dob','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email','phone','first_name','last_name')
    ordering = ('email',)

    def employee_application(self,obj):
        url =  reverse('admin:employee_employee_change',args=(obj.employee.pk,))
        return format_html("<a href='{url}'>application</a>",url=url)

    def lifeguard_application(self,obj):
        url =  reverse('admin:lifeguard_lifeguard_change',args=(obj.lifeguard.pk,))
        return format_html("<a href='{url}'>application</a>",url=url)

    def is_hired_employee(self,obj):
        return obj.employee.is_hired

admin.site.register(User, CustomUserAdmin)
admin.site.register(EmergencyContact)
admin.site.register(Address)



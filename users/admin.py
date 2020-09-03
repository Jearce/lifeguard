from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User,EmergencyContact,Address


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email','first_name', 'last_name','age','phone','is_staff', 'is_active','is_employee','is_lifeguard')
    list_filter = ('email', 'is_staff', 'is_active','is_employee','is_lifeguard')
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


admin.site.register(User, CustomUserAdmin)
admin.site.register(EmergencyContact)
admin.site.register(Address)



from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('home/',views.HomeView.as_view(),name='home'),
    path('lifeguard-registration/contact-information/<int:pk>/',views.ContactInformationUpdate.as_view(),name='contact_information'),
    path('lifeguard-registration/emergency-contact-create/',views.EmergencyContactCreate.as_view(),name='emergency_contact_create'),
    path('lifeguard-registration/address/',views.AddressCreate.as_view(),name='address'),
    path('lifeguard-registration/lifeguard-information/',views.LifeguardCreate.as_view(),name='lifeguard_create'),
    path('lifeguard/classes/',views.LifeguardClasses.as_view(),name='classes'),
    path('lifeguard/classes/<int:pk>/',views.LifeguardClasses.as_view(),name='classes')
]

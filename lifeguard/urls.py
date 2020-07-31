from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('home/',views.HomeView.as_view(),name='home'),
    path('lifeguard-registration/contact-information/<int:pk>/',views.ContactInformationUpdate.as_view(),name='contact_information'),
    path('lifeguard-registration/emergency-contact/',views.EmergencyContactCreate.as_view(),name='emergency_contact'),
    path('lifeguard-registration/address/',views.AddressCreate.as_view(),name='address')
]

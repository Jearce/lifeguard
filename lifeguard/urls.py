from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('home/',views.HomeView.as_view(),name='home'),
    path('lifeguard-registration/contact-information',views.ContactInformationView.as_view(),name='contact_information')
]

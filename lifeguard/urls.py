from django.contrib import admin
from django.urls import path

from . import views

app_name = 'lifeguard'
urlpatterns = [
    path('create/',views.LifeguardCreateOrUpdate.as_view(),name='create'),
    path('already-certified/',views.LifeguardCertified.as_view(),name='already_certified'),
    path('classes/',views.LifeguardClasses.as_view(),name='classes'),
    path('classes/<int:pk>/',views.LifeguardClasses.as_view(),name='classes'),
    path('enrolled-classes/',views.EnrolledClasses.as_view(),name='enrolled_classes'),
    path('registration/',views.lifeguard_registration,name='registration'),
]

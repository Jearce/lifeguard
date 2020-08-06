from django.contrib import admin
from django.urls import path

from . import views

app_name = 'lifeguard'
urlpatterns = [
    path('create/',views.LifeguardCreateOrUpdate.as_view(),name='create'),
    path('classes/',views.LifeguardClasses.as_view(),name='classes'),
    path('classes/<int:pk>/',views.LifeguardClasses.as_view(),name='classes')
]

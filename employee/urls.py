from django.urls import path
from . import views

app_name = 'employee'
urlpatterns = [
    path('create/',views.EmployeeUpdate.as_view(),name="create"),
]

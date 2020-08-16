from django.urls import path
from . import views

app_name = 'employee'
urlpatterns = [
    path('create/',views.EmployeeCreateOrUpdate.as_view(),name="create"),
    path('education/',views.EmployeeEducation.as_view(),name="education"),
    path('job-history/',views.JobHistory.as_view(),name="job_history"),
    path('registration/',views.employee_registration,name="registration")
]

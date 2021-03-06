from django.urls import path
from . import views

app_name = 'employee'
urlpatterns = [
    path('create/',views.EmployeeCreateOrUpdate.as_view(),name="create"),
    path('education/',views.EmployeeEducation.as_view(),name="education"),
    path('job-history/',views.JobHistory.as_view(),name="job_history"),
    path('registration/',views.employee_registration,name="registration"),
    path('application-status/',views.ApplicationStatus.as_view(),name="application_status"),
    path('employee-checklist/',views.EmployeeChecklist.as_view(),name="checklist"),
    path('positions/',views.get_positions,name="positions"),
    path('employees',views.get_employees,name="employees"),
]

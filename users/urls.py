from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'
urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('login/',views.LogInView.as_view(),name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('password_reset/',views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_done/',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_complete/',views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),

    path('contact-information/<int:pk>/',views.ContactInformationUpdate.as_view(),name='contact_information'),
    path('emergency-contact/',views.EmergencyContactCreateOrUpdate.as_view(),name='emergency_contact'),
    path('address/',views.AddressCreateOrUpdate.as_view(),name='address'),
]

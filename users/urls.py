from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app = 'users'
urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('login/',views.LogInView.as_view(),name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             subject_template_name="users/password_reset_subject.txt",
             email_template_name="users/password_reset_email.html"
         ),
         name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html"
         ),
         name='password_reset_confirm'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="users/password_reset_done.html"
         ),
         name='password_reset_done'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="users/password_reset_complete.html"),
         name='password_reset_complete')
]

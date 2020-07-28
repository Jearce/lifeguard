from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app = 'users'
urlpatterns = [
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('login/',views.LogInView.as_view(),name='login'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset')
]

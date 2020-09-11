from django.urls import path

from payment import views

app_name = "payment"
urlpatterns = [
    path('new/',view.new_checkout,name="new_checkout"),

]

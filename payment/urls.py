from django.urls import path

from payment import views

app_name = "payment"
urlpatterns = [
    path("lifeguard-class/",views.EnrollmentCart.as_view(),name="lifeguard_class"),

    #path('new/',views.new_checkout,name="new_checkout"),
    #path('checkout/<transaction_id>',views.show_checkout,name="show_checkout"),
    #path("checkout/",views.create_checkout,name="create_checkout"),
]

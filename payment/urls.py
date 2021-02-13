from django.urls import path

from payment import views

app_name = "payment"
urlpatterns = [
    path("enrollment-cart/",views.EnrollmentCart.as_view(),name="enrollment_cart"),
    path("enrollment-cart/<int:pk>",views.EnrollmentCart.as_view(),name="drop_enrollment"),
    path("lifeguard-checkout/",views.LifeguardCheckout.as_view(),name="lifeguard_checkout"),
    path("lifeguard-checkout/process-payment",views.process_payment,name="process_payment"),
    path('checkout/<transaction_id>',views.show_checkout,name="show_checkout")
]

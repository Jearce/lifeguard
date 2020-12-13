from django.urls import path

from payment import views

app_name = "payment"
urlpatterns = [
    path("enrollment-cart/",views.EnrollmentCart.as_view(),name="enrollment_cart"),
    path("enrollment-cart/<int:pk>",views.EnrollmentCart.as_view(),name="drop_enrollment"),
    path("lifeguard-checkout/",views.LifeguardCheckout.as_view(),name="lifeguard_checkout"),

    #path('new/',views.new_checkout,name="new_checkout"),
    #path('checkout/<transaction_id>',views.show_checkout,name="show_checkout"),
    #path("checkout/",views.create_checkout,name="create_checkout"),
]

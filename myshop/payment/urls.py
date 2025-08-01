from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('razorpay-checkout/', views.razorpay_checkout, name='razorpay_checkout'),
    path('verify/', views.verify_payment, name='verify'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
]

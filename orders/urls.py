from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_order, name="create_order"),         
    path("my-orders/", views.my_orders, name="my_orders"),            
    path("<int:pk>/", views.order_detail, name="order_detail"),        
    path("<int:pk>/cancel/", views.cancel_order, name="cancel_order"), 
    path("<int:pk>/pay/", views.pay_order, name="pay_order"),
]
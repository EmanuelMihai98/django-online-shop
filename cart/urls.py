from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.get_cart, name="get_cart"),
    path("cart/add/", views.add_cart, name="add_cart"),
    path("cart/decrease/", views.decrease_cart, name="decrease_cart"),
    path("cart/remove/", views.remove_cart, name="remove_cart"),
]
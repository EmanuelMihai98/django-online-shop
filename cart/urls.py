from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_cart, name="get_cart"),
    path("add/", views.add_cart, name="add_cart"),
    path("decrease/", views.decrease_cart, name="decrease_cart"),
    path("remove/", views.remove_cart, name="remove_cart"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/', views.update_cart_quantity, name="update_cart_quantity"),
    path("delete/", views.delete_from_cart, name="delete_from_cart"),
    



    path("", views.get_cart, name="get_cart"),
    path("add/", views.add_cart, name="add_cart"),
    path("decrease/", views.decrease_cart, name="decrease_cart"),
    path("remove/", views.remove_cart, name="remove_cart"),
]
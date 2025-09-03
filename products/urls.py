from django.urls import path
from .views import products_list, get_product, add_product, update_product, delete_product

urlpatterns = [
    path("", products_list, name="products_list"),
    path("<int:pk>/", get_product, name="get_product"),
    path("add/", add_product, name="add_product"),
    path("<int:pk>/update/", update_product, name="update_product"),
    path("<int:pk>/delete/", delete_product, name="delete_product")
]
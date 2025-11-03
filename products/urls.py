from django.urls import path
from .views import products_list, get_product, add_product, update_product, delete_product, product_list_page, get_product_page, add_product_page, update_product_page, delete_product_page

urlpatterns = [
    path("page/", product_list_page, name="products_list_page"),
    path("<slug:slug>/", get_product_page, name ="get_product_page" ),
    path("add/", add_product_page, name="add_product_page"),
    path("<int:pk>/update/", update_product_page, name ="update_product_page"),
    path("<int:pk>/delete/", delete_product_page, name = "delete_product_page" ),

    path("api/", products_list, name="products_list_api"),
    path("api/<int:pk>/", get_product, name="get_product_api"),
    path("api/add/", add_product, name="add_product_api"),
    path("api/<int:pk>/update/", update_product, name="update_product_api"),
    path("api/<int:pk>/delete/", delete_product, name="delete_product_api")


  
]
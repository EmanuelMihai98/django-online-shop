from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from products.models import Product
from .cart import Cart

@api_view(["POST"])
def add_cart(request):
    product_id = request.data.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product)

    response_data = {
        "items": cart.items(),
        "total": cart.total()
    }
    return Response(response_data, status=201)

@api_view(["PATCH"])
def decrease_cart(request):
    product_id = request.data.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.decrease(product)

    response_data = {
        "items": cart.items(),
        "total": cart.total()
    }
    return Response(response_data, status=200)

@api_view(["DELETE"])
def remove_cart(request):
    product_id = request.data.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)

    response_data = {
        "items": cart.items(),
        "total": cart.total()
    }
    return Response(response_data, status=200)

@api_view(["GET"])
def get_cart(request):
    cart = Cart(request)
    
    response_data = {
        "items": cart.items(),
        "total": cart.total()
    }
    return Response(response_data, status=200)



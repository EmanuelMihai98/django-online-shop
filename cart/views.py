from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect
from products.models import Product
from .cart import Cart
import datetime


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

@require_POST
def add_to_cart(request):

    cart =request.session.get("cart", {})

    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 1))

    if not product_id:
        return redirect("product_list_page")
    
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str]["quantity"] += quantity
        cart[product_id_str]["timestamp"] = str(datetime.datetime.now())

    else:
        cart[product_id_str] = {
            "quantity":quantity,
            "timestamp": str(datetime.datetime.now())
        }

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("view_cart")


def view_cart(request):
    try:
        cart = request.session.get("cart", {})
        total = 0 
        cart_items = []

        for product_id, item_data in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                quantity = item_data["quantity"]
                subtotal = product.price * quantity
                total += subtotal

                cart_items.append({
                    "id": product_id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": quantity,
                    "subtotal": subtotal,
                    "product_object": product
                })
            except Product.DoesNotExist:
                pass
            except Exception as e:
                print(f"ERROR item: {e}")

        context = {
            "cart_items": cart_items,
            "total": total
        }

        return render(request, "cart.html", context)
    
    except Exception as e:
        print(f"MAJOR ERROR in view_cart: {e}")
        import traceback
        traceback.print_exc()
        raise

@require_POST
def update_cart_quantity(request):
    cart = request.session.get("cart", {})
    product_id = request.POST.get("product_id")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    product_id_str = str(product_id)

    if product_id_str in cart:
        if quantity > 0:
            cart[product_id_str]["quantity"] = quantity
        else:
            del cart[product_id_str]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("view_cart")

@require_POST
def delete_from_cart(request):
    cart = request.session.get("cart", {})
    product_id = request.POST.get("product_id")
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("view_cart")
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product
from .serializers import OrderSerializer, OrderCreateSerializer
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

@api_view(["POST"])
@permission_classes([IsAuthenticated])  # doar user logat poate comanda
def create_order_api(request):
    serializer = OrderCreateSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    order = serializer.save()
    # când returnezi, folosești OrderSerializer (ca să vezi și sumele, items etc.)
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return Response(OrderSerializer(orders, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return Response(OrderSerializer(order).data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status != Order.Status.PENDING:
        return Response({"detail": "Order cannot be canceled."}, status=status.HTTP_400_BAD_REQUEST)
    order.status = Order.Status.CANCELED
    order.save(update_fields=["status"])
    return Response(OrderSerializer(order).data)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def pay_order(request, pk):
    with transaction.atomic():
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if order.status != Order.Status.PENDING:
            return Response({"error": "Order cannot be paid"}, status=400)
        
        order.status = Order.Status.PAID
        order.save(update_fields=["status"])
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=200)


@login_required 
def create_order(request):
  
    cart = request.session.get('cart', {})
    
   
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('products_list_page') 

    if request.method == 'POST':
       
        form = OrderCreateForm(request.POST)
        if form.is_valid():
           
            order = form.save(commit=False)
            order.user = request.user 
            
            
            subtotal = Decimal('0.00')
            items_to_create = []
            
            for product_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    quantity = item_data['quantity']
                    item_total = product.price * quantity
                    subtotal += item_total
                    
                    
                    items_to_create.append(OrderItem(
                        
                        product=product,
                        product_name=product.name, 
                        price=product.price,       
                        quantity=quantity,
                        total=item_total
                    ))
                except Product.DoesNotExist:
                    messages.error(request, f"A product from your cart is not available anymore")
                    return redirect('view_cart') 

            
            shipping_cost = Decimal('15.00') 
            order.subtotal = subtotal
            order.shipping = shipping_cost
            order.total = subtotal + shipping_cost
            
            
            order.save()
            
            
            for item in items_to_create:
                item.order = order 
            
          
            OrderItem.objects.bulk_create(items_to_create)
            
            # (7) GOLIM COȘUL
            del request.session['cart']
            request.session.modified = True
            
            return redirect('order_success_page')

    else:
  
        form = OrderCreateForm()
    
    context = {
        'form': form
    }
    return render(request, 'orders/checkout.html', context)



@login_required
def order_success(request):
 
    return render(request, 'orders/order_success.html')
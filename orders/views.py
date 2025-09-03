from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])  # doar user logat poate comanda
def create_order(request):
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

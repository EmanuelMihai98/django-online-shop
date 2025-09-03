from decimal import Decimal
from rest_framework import serializers
from products.models import Product
from .models import Order, OrderItem

def calculate_shipping(order) -> Decimal:
    if order.subtotal >= Decimal("200.00"):
        return Decimal("0.00")
    else:
        return Decimal("15.00")
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "product_name", "price", "quantity", "total"]
        read_only_fields = ["product_name", "price", "total"]


class OrderSerializer(serializers.ModelSerializer):
    username =serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "username", "email", "full_name", "address", "phone", "subtotal", "shipping",
                  "total", "created_at", "items"]
        read_only_fields = ["id", "status", "username", "email", "full_name","subtotal", "shipping",
                  "total", "created_at", "items"]
    def get_full_name(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name
    
class OrderCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, max_length=15)
    address = serializers.CharField(required=True)

    class Meta:
        model = Order
        fields = ["phone", "address"]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        session = request.session

        cart = session.get("cart") or {}
        if not cart:
            raise serializers.ValidationError({"cart": "Cart is empty"})
        
        order = Order.objects.create(
            user=user,
            status=Order.Status.PENDING,
            address=validated_data["address"],
            phone=validated_data["phone"],
            subtotal=Decimal("0.00"),
            shipping=Decimal("0.00"),
            total=Decimal("0.00")
        )

        subtotal = Decimal("0.00")
        for product_id, item in cart.items():
            product = Product.objects.get(pk=int(product_id))
            quantity = int(item.get("quantity", 1))
            unit_price = product.price
            line_total = unit_price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            quantity=quantity,
            price=unit_price,
            total=line_total
        )
        subtotal += line_total
    
        order.subtotal =subtotal
        order.shipping = calculate_shipping(order)
        order.total = order.subtotal + order.shipping
        order.save()

        request.session["cart"] = {}
        request.session.modified =True
        return order
    
   
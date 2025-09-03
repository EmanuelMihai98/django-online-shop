from django.conf import settings
from products.models import Product
from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            self.session[settings.CART_SESSION_ID] = {}
            cart = self.session[settings.CART_SESSION_ID]
        self.cart = cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
        self.cart[product_id]["quantity"] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]["quantity"] > 1:
                self.cart[product_id]["quantity"] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    
    def items(self):
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        result = []
        for product in products:
            product_id = str(product.id)
            quantity = self.cart[product_id]["quantity"]
            price = product.price
            total = price * quantity
            result.append({
                "id": product.id,
                "name": product.name,
                "price": str(price),
                "quantity": quantity,
                "total": str(total)
            })
        result.sort(key=lambda x: x["id"])
        return result
    
    def total(self):
        total_sum = Decimal("0.00")
        for item in self.items():
            total_sum += Decimal(item["total"])
        return str(total_sum)

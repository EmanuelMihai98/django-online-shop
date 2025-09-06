from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from products.models import Product, Category
from orders.models import Order, OrderItem

User = get_user_model()

class OrderApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mihai", password="Str0ng!23")
        self.other = User.objects.create_user(username="other", password="Str0ng!23")
        self.client.login(username="mihai", password="Str0ng!23")

        self.category = Category.objects.create(name="Food", slug="food")

        self.product = Product.objects.create(name="Pizza", price=Decimal("50.00"), category=self.category)

        self.create_url=reverse("create_order")
        self.my_orders_url=reverse("my_orders")
        session = self.client.session
        session["cart"] = {
            str(self.product.id):{
                "quantity": 2,
            }  
        }
        session.save()

    def test_create_order_ok(self):
        payload= {"phone": "0712345678",
                  "address": "Bucuresti, Str. Test 1"}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

        created = Order.objects.get(id=response.data["id"])
        self.assertEqual(created.user, self.user)
        self.assertEqual(created.items.count(), 1)

        item = created.items.first()
        self.assertEqual(item.product_id, self.product.id)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, self.product.price)
        self.assertEqual(item.total, self.product.price * item.quantity)
        self.assertEqual(created.subtotal, self.product.price * item.quantity)
        self.assertEqual(created.shipping, Decimal("15.00"))
        self.assertEqual(created.total, created.subtotal + created.shipping)


    def test_order_detail_other_blocked(self):
       order = Order.objects.create(user=self.other, status=Order.Status.PENDING)
       url = reverse("order_detail", args=[order.id])
       response = self.client.get(url, format="json")
       self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_cancel_order_ok(self):
        order = Order.objects.create(user=self.user, status=Order.Status.PENDING)
        url=reverse("cancel_order", args=[order.id])

        response=self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.CANCELED)

    def test_cancel_order_not_pending(self):
        order = Order.objects.create(user=self.user, status=Order.Status.PAID)
        url = reverse("cancel_order", args=[order.id])
        response = self.client.patch(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
        
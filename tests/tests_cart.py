from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product, Category

class CartApiTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="default name")
        self.product= Product.objects.create(
            name="Test Product",
            price=Decimal("10.00"),
            slug="test-product",
            category= self.category
        )
      
        self.get_url = reverse("get_cart")
        self.add_url = reverse("add_cart")
        self.decrease_url = reverse("decrease_cart")
        self.remove_url = reverse("remove_cart")
        
    def test_cart_initially_empty(self):
        response = self.client.get(self.get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["items"], [])
        self.assertEqual(response.data["total"], "0.00")

    def test_add_by_one(self):
        response = self.client.post(self.add_url, {"product_id": self.product.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total"], "10.00")
        self.assertEqual(len(response.data["items"]), 1)

        item = response.data["items"][0]
        self.assertEqual(item["id"], self.product.id)
        self.assertEqual(item["name"], "Test Product")
        self.assertEqual(item["price"], "10.00")
        self.assertEqual(item["quantity"], 1)
        self.assertEqual(item["total"], "10.00")

        response = self.client.post(self.add_url, {"product_id": self.product.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total"], "20.00")
        self.assertEqual(response.data["items"][0]["quantity"], 2)

    def test_decrease_by_one(self):
        self.client.post(self.add_url, {"product_id": self.product.id}, format="json")
        self.client.post(self.add_url, {"product_id": self.product.id}, format="json")

        response = self.client.patch(self.decrease_url, {"product_id": self.product.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], "10.00")
        self.assertEqual(response.data["items"][0]["quantity"], 1)

        response = self.client.patch(self.decrease_url, {"product_id": self.product.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["items"], [])
        self.assertEqual(response.data["total"], "0.00")

    def test_remove_directly(self):
        self.client.post(self.remove_url, {"product_id": self.product.id}, format="json")

        response = self.client.delete(self.remove_url, {"product_id": self.product.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["items"], [])
        self.assertEqual(response.data["total"], "0.00")

    def test_get_404_cart(self):
         response = self.client.post(self.add_url, {}, format="json")
         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product, Category

        

class ProductApiTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Default category")
        self.product = Product.objects.create(
            name="Test Product",
            price="99.99",
            slug="test-product",
            category=self.category,
        )
        self.list_url   = reverse("products_list")                           
        self.detail_url = reverse("get_product", args=[self.product.id])     
        self.create_url = reverse("add_product")                             
        self.update_url = reverse("update_product", args=[self.product.id])  
        self.delete_url = reverse("delete_product", args=[self.product.id])  


    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

   
    def test_get_product(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

   
    def test_create_product(self):
        payload = {
            "name": "New Product",
            "price": "49.99",
            "slug": "new-product",
            "category": self.category.id,
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name="New Product").exists())


    def test_update_product(self):
        payload = {
            "name": "Updated Product",
            "price": "99.99",
            "category": self.category.id,
        }
        response = self.client.put(self.update_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.slug, "updated-product")

  
    def test_delete_product(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())



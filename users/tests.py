from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserTestApi(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login_view")
        self.logout_url = reverse("logout_view")
        self.me_url = reverse("me")
        self.change_password_url = reverse("change_password")

        self.user = User.objects.create(
            username = "Mihai",
            email = "mihai@yahoo.com",
            password = "Str0ngPassword123!",
        )

    def test_register_succes(self):
        response = self.client.post(self.register_url,{
            "username": "anotheruser",
            "email": "anothermail@yahoo.com",
            "password": "Str0ngPassword!23",
            "confirm_password": "Str0ngPassword!23",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "anotheruser")

    def test_username_duplicate(self):
        response = self.client.post(self.register_url, {
            "username": "Mihai",
            "email": "newEmail",
            "password": "Str0ngPassword!23",
            "confirm_password": "Str0ngPassword!23",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_email_duplicate(self):
        response = self.client.post(self.register_url, {
            "username": "Mihai",
            "email": "mihai@yahoo.com",
            "password": "Str0ngPassword!23",
            "confirm_password": "Str0ngPassword!23",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_login(self):
        response = self.client.post(self.login_url, {
            "username":"Mihai",
            "email":"mihai@yahoo.com",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.me_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "mihai")

    def test_logout(self):
        self.client.post(self.login_url, {
           "username":"Mihai",
           "password": "Str0ngPassword!23",
        }, format="json")
        
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_me_requires_auth(self):
        self.client.post(self.logout_url, format="json")
        response = self.client.get(self.me_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password(self):
        self.client.post(self.login_url, {
           "username":"Mihai",
           "password": "Str0ngPassword!23",
           }, format="json")
        
        response = self.client.post(self.change_password_url, {
           "password": "Str0ngPassword!23",
           "new_password": "Str0ngPassword!123"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

        self.client.post(self.logout_url, format="json")
        response = self.client.post(self.login_url,{
            "username":"Mihai",
            "password": "Str0ngPassword!123"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("username", response.data)
        

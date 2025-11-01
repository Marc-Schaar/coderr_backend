from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User


class TestLogin(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="exampleUsername",
            password="examplePassword",
            email="email@mail.de",
        )

    def test_login_user_200(self):
        url = reverse("login-list")
        user_client = APIClient()
        data = {"username": "exampleUsername", "password": "examplePassword"}

        response = user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["user_id"], 1)
        self.assertEqual(response.data["email"], self.user.email)

    def test_login_user_400(self):
        url = reverse("login-list")
        user_client = APIClient()

        data = {"username": "", "password": "examplePassword"}

        response = user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_400(self):
        url = reverse("login-list")
        user_client = APIClient()
        data = {"username": "exampleUsername", "password": ""}

        response = user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

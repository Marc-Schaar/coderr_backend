from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User

class TestRegistration(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="exampleUsername", password="examplePassword")
        # self.token_user = Token.objects.create(user=self.user)
      
        # self.user_client = APIClient()
        # self.user_client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user.key)

    
      

    def test_login_user(self):
        url = reverse("login-list")
        user_client = APIClient()
        data = {
        "username": "exampleUsername",
        "password": "examplePassword"
        }

        response = user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
        "username": "",
        "password": "examplePassword"
        }

        response = user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
        "username": "exampleUsername",
        "password": ""
        }

        response = user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

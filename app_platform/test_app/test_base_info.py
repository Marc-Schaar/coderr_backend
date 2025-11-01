from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User


class TestBaseInfo(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="exampleUsername", password="examplePassword"
        )
        self.client_user_1 = APIClient()

    def test_baseinfo_get_200(self):
        url = reverse("base-info")
        response = self.client_user_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("review_count", data)
        self.assertIn("average_rating", data)
        self.assertIn("business_profile_count", data)
        self.assertIn("offer_count", data)

        self.assertIsInstance(data["review_count"], int)
        self.assertIsInstance(data["average_rating"], float)
        self.assertIsInstance(data["business_profile_count"], int)
        self.assertIsInstance(data["offer_count"], int)

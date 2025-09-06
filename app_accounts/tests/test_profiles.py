from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User

class TestProfiles(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username="max_mustermann", password="examplePassword", email="test@test.de", type="business")
        self.user_2 = User.objects.create_user(username="exampleUsername_2", password="examplePassword")

        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.token_user_2 = Token.objects.create(user=self.user_2)

        self.user_client_1 = APIClient()
        self.user_client_1.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1.key)

        self.user_client_2 = APIClient()
        self.user_client_2.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_2.key)

    def test_profiles_get(self):
        url = reverse("profile-detail", kwargs={"pk": 1})
        response = self.user_client_1.get(url, format="json")
        expected_data = {
            "id": 1,
            "username": "max_mustermann",
            "first_name": "",
            "last_name": "",
            "file": None,
            "location": "",   
            "tel": "",
            "description": "",
            "working_hours": "",
            "type": "business",
            "email": "test@test.de",
            "created_at": response.data["created_at"],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
      

       
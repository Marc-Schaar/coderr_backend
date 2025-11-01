from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestRegistration(APITestCase):
    def setUp(self):
        self.user_client = APIClient()
        self.url = reverse("registration-list")
        self.data = {
            "username": "user_test",
            "email": "user@mail.de",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer",
        }

    def test_register_user_success(self):
        response = self.user_client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertIn("token", response_data)
        self.assertEqual(response_data["username"], "user_test")
        self.assertEqual(response_data["email"], "user@mail.de")
        self.assertEqual(response_data["user_id"], 1)

    def test_register_user_exist(self):
        self.user_client.post(self.url, self.data, format="json")
        response = self.user_client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "Ungültige Anfragedaten.")

    def test_register_user_invalid_data(self):
        invalid_data_list = [
            {
                "username": "",
                "email": "user@mail.de",
                "password": "password123",
                "repeated_password": "password123",
                "type": "customer",
            },
            {
                "username": "user",
                "email": "",
                "password": "password123",
                "repeated_password": "password123",
                "type": "customer",
            },
            {
                "username": "user",
                "email": "user@mail.de",
                "password": "password123",
                "repeated_password": "456",
                "type": "customer",
            },
            {
                "username": "user",
                "email": "user@mail.de",
                "password": "password123",
                "repeated_password": "password123",
                "type": "",
            },
        ]
        for data in invalid_data_list:
            with self.subTest(data=data):
                response = self.user_client.post(self.url, data, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("error", response.json())
                self.assertEqual(response.json()["error"], "Ungültige Anfragedaten.")

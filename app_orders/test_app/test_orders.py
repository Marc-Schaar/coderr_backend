from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User
from app_orders.models import Order


class TestProfiles(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="jdoe", password="examplePassword", email="test@test.de", type="business", first_name="John", last_name="Doe")
        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.user_client_1 = APIClient()
        self.user_client_1.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1.key)

        self.user_2 = User.objects.create_user(
            username="mschaar", password="examplePassword", email="test2@test.de", type="customer", first_name="Marc", last_name="Schaar")
        self.token_user_2 = Token.objects.create(user=self.user_2)
        self.user_client_2 = APIClient()
        self.user_client_2.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_2.key)

        self.user_3 = User.objects.create_user(
            username="User3", password="testpassword", email="test3@test.de", type="customer", first_name="User", last_name="Test"
        )

        self.order_1 = Order.objects.create(
            customer_user=self.user_2,
            business_user=self.user_1,
            revisions=2,
            delivery_time_in_days=5,
            price=150,
            features={"feature1": "value1", "feature2": "value2"},
            offer_type="standard",
            status="pending"
        )

        self.order_2 = Order.objects.create(
            customer_user=self.user_2,
            business_user=self.user_1,
            revisions=1,
            delivery_time_in_days=3,
            price=100,
            features={"featureA": "valueA"},
            offer_type="basic",
            status="in_progress"
        )


class Test_Offer(TestProfiles):
    maxDiff = None

    def test_order_list_get_200(self):
        url = reverse("order-list")
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        for data in response_data:
            self.assertIsInstance(data, dict)
            self.assertIn('id', data)
            self.assertIn('customer_user', data)
            self.assertIn('business_user', data)
            self.assertIn('revisions', data)
            self.assertIn('delivery_time_in_days', data)
            self.assertIn('price', data)
            self.assertIn('features', data)
            self.assertIn('offer_type', data)
            self.assertIn('status', data)
            self.assertIn('created_at', data)
            self.assertIn('updated_at', data)

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User
from app_orders.models import Order
from app_offers.models import Offer, OfferDetails


class TestOrders(APITestCase):
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
        self.token_user_3 = Token.objects.create(user=self.user_3)
        self.user_client_3 = APIClient()
        self.user_client_3.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_3.key)

        self.user_admin = User.objects.create_user(
            username="UserAdmin", password="testpassword", email="test4@test.de", type="customer", first_name="User", last_name="Admin", is_staff=True
        )
        self.token_user_admin = Token.objects.create(user=self.user_admin)
        self.user_client_admin = APIClient()
        self.user_client_admin.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_admin.key)

        self.offer_1 = Offer.objects.create(
            user=self.user_1,
            title="Website Design",
            description="Professionelles Website-Design...",
            min_price=1000,
            min_delivery_time=7,
        )

        self.offer_detail_1 = OfferDetails.objects.create(
            offer_id=1,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic"
        )

        self.order_1 = Order.objects.create(
            customer_user=self.user_2,
            business_user=self.user_1,
            revisions=2,
            delivery_time_in_days=5,
            price=150,
            features={"feature1": "value1", "feature2": "value2"},
            offer_type="standard",
            status="in_progress"
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
        self.order_3 = Order.objects.create(
            customer_user=self.user_3,
            business_user=self.user_1,
            revisions=3,
            delivery_time_in_days=7,
            price=200,
            features={"featureX": "valueX", "featureY": "valueY"},
            offer_type="premium",
            status="completed"
        )

    def test_order_list_get_200_as_customer_user(self):
        url = reverse("order-list")
        response = self.user_client_2.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 2)
        for data in response_data:
            self.assertIsInstance(data, dict)
            self.assertIn('id', data)
            self.assertIn('customer_user', data)
            self.assertIn('business_user', data)
            self.assertIn('title', data)
            self.assertIn('revisions', data)
            self.assertIn('delivery_time_in_days', data)
            self.assertIn('price', data)
            self.assertIn('features', data)
            self.assertIn('offer_type', data)
            self.assertIn('status', data)
            self.assertIn('created_at', data)
            self.assertIn('updated_at', data)

        response = self.user_client_3.get(url)
        self.assertEqual(len(response.json()), 1)

    def test_order_list_get_200_as_business_user(self):
        url = reverse("order-list")
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 3)

    def test_order_list_get_401(self):
        url = reverse("order-list")
        self.user_client_1.logout()
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_list_post_201(self):
        url = reverse("order-list")
        payload = {"offer_detail_id": self.offer_detail_1.id}
        response = self.user_client_2.post(url, payload, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('id', response_data)
        self.assertIn('customer_user', response_data)
        self.assertIn('business_user', response_data)
        self.assertIn('title', response_data)
        self.assertIn('revisions', response_data)
        self.assertIn('delivery_time_in_days', response_data)
        self.assertIn('price', response_data)
        self.assertIn('features', response_data)
        self.assertIn('offer_type', response_data)
        self.assertIn('status', response_data)
        self.assertIn('created_at', response_data)
        self.assertIn('updated_at', response_data)

    def test_order_list_post_400(self):
        url = reverse("order-list")
        payload = {}
        response = self.user_client_2.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_list_post_401(self):
        url = reverse("order-list")
        payload = {"offer_detail_id": self.offer_detail_1.id}
        self.user_client_2.logout()
        response = self.user_client_2.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_list_post_403(self):
        url = reverse("order-list")
        payload = {"offer_detail_id": self.offer_detail_1.id}
        response = self.user_client_1.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_list_post_404(self):
        url = reverse("order-list")
        payload = {"offer_detail_id": 9999}
        response = self.user_client_2.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail_patch_200(self):
        url = reverse("order-detail", kwargs={"pk": self.order_1.id})
        payload = {"status": "completed"}
        response = self.user_client_1.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order_1.refresh_from_db()
        self.assertEqual(self.order_1.status, "completed")

    def test_order_detail_patch_401(self):
        url = reverse("order-detail", kwargs={"pk": self.order_1.id})
        payload = {"status": "completed"}
        self.user_client_1.logout()
        response = self.user_client_1.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_detail_patch_403(self):
        url = reverse("order-detail", kwargs={"pk": self.order_1.id})
        payload = {"status": "completed"}
        response = self.user_client_2.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_detail_patch_404(self):
        url = reverse("order-detail", kwargs={"pk": 999999})
        payload = {"status": "completed"}
        response = self.user_client_2.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail_delete_204(self):
        url = reverse("order-detail", kwargs={"pk": self.order_1.id})
        response = self.user_client_admin.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=self.order_1.id)

    def test_order_detail_delete_401(self):
        url = reverse("order-detail", kwargs={"pk": self.order_1.id})
        self.user_client_1.logout()
        response = self.user_client_1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_detail_delete_403(self):
        url = reverse("order-detail", kwargs={"pk": self.order_1.id})
        response = self.user_client_1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_detail_delete_404(self):
        url = reverse("order-detail", kwargs={"pk": 99999})
        response = self.user_client_1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_count_view_200(self):
        url = reverse("order-count", kwargs={"pk": self.user_1.id})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIn("order_count", response_data)
        self.assertEqual(response_data["order_count"], 2)

    def test_order_count_view_401(self):
        url = reverse("order-count", kwargs={"pk": self.user_1.id})
        self.user_client_1.logout()
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_order_count_view_404(self):
        url = reverse("order-count", kwargs={"pk": self.user_2.id})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_completed_order_count_view_200(self):
        url = reverse("completed-order-count", kwargs={"pk": self.user_1.id})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("completed_order_count", response_data)
        self.assertEqual(response_data["completed_order_count"], 1)
    
    def test_completed_order_count_view_401(self):
        url = reverse("completed-order-count", kwargs={"pk": self.user_1.id})
        self.user_client_1.logout()
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_completed_order_count_view_404(self):
        url = reverse("completed-order-count", kwargs={"pk": self.user_2.id})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User
from app_offers.models import Offer

from app_offers.api.serializers import OfferSerializer


class TestProfiles(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="jdoe", password="examplePassword", email="test@test.de", type="business", first_name="John", last_name="Doe")
        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.user_client_1 = APIClient()
        self.user_client_1.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1.key)

        self.user_2 = User.objects.create_user(
            username="mschaar", password="examplePassword", email="test2@test.de", type="business", first_name="Marc", last_name="Schaar")
        self.token_user_2 = Token.objects.create(user=self.user_2)
        self.user_client_2 = APIClient()
        self.user_client_2.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_2.key)

        self.offer_1 = Offer.objects.create(
            user=self.user_1,
            title="Website Design",
            description="Professionelles Website-Design...",
            min_price=100,
            min_delivery_time=7,
        )

        self.offer_2 = Offer.objects.create(
            user=self.user_1,
            title="Website Design 2",
            description="Professionelles Website-Design...",
            min_price=1000,
            min_delivery_time=70,
        )

        self.offer_3 = Offer.objects.create(
            user=self.user_1,
            title="Website Design 3",
            description="Professionelles Website-Design...",
            min_price=10000,
            min_delivery_time=700,
        )


class Test_Offer_List(TestProfiles):
    maxDiff = None

    def test_offer_list(self):
        url = reverse("offer-list")
        response = self.user_client_1.get(url)

        expected_dict = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": OfferSerializer([self.offer_1, self.offer_2, self.offer_3], many=True).data
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_list_filter_by_creator_id_200(self):
        url = reverse("offer-list") + f"?creator_id={self.user_1.id}"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_dict = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": OfferSerializer([self.offer_1, self.offer_2, self.offer_3], many=True).data
        }
        self.assertDictEqual(response.json(), expected_dict)

        url = reverse("offer-list") + f"?creator_id={self.user_2.id}"
        response = self.user_client_1.get(url)
        expected_dict = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_list_filter_by_creator_id_400(self):
        url = reverse("offer-list") + f"?creator_id={99}"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_list_filter_by_min_price_200(self):
        url = reverse("offer-list") + f"?min_price=1000000"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_dict = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }
        self.assertDictEqual(response.json(), expected_dict)

        url = reverse("offer-list") + f"?min_price=100"
        response = self.user_client_1.get(url)
        expected_dict = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": OfferSerializer([self.offer_1, self.offer_2, self.offer_3], many=True).data
        }
        self.assertDictEqual(response.json(), expected_dict)

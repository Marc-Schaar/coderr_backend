from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User
from app_offers.models import Offer

class TestProfiles(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username="jdoe", password="examplePassword", email="test@test.de", type="business")
        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.user_client_1 = APIClient()
        self.user_client_1.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1.key)

        self.offer_1 = Offer.objects.create(user=self.user_1, title="Website Design", description="Professionelles Website-Design...", min_price=100, min_delivery_time=7)


class Test_Offer_List(TestProfiles):
    def test_offer_list(self):
        url = reverse("offer-list")
        response = self.client.get(url)
        print("Response Offers; ",response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            # "count": 1,
            # "next": "http://127.0.0.1:8000/api/offers/?page=2",
            # # "previous": null,
            # "results": [
                # {
                "id": 1,
                "user": 1,
                "title": "Website Design",
                "image": None,
                "description": "Professionelles Website-Design...",
                "created_at": response.data[0]["created_at"],
                "updated_at": response.data[0]["updated_at"],
                # "details": [
                #     {
                #     "id": 1,
                #     "url": "/offerdetails/1/"
                #     },
                #     {
                #     "id": 2,
                #     "url": "/offerdetails/2/"
                #     },
                #     {
                #     "id": 3,
                #     "url": "/offerdetails/3/"
                #     }
                # ],
                "details": None,
                "min_price": 100,
                "min_delivery_time": 7,
                "user_details": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "jdoe"
                }
                }
            # ]
        # }
        
        self.assertJSONEqual(response.content, [expected_data])

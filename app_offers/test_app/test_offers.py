from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User
from app_offers.models import Offer, OfferDetails

from app_offers.api.serializers import OfferListSerializer


class TestOffer(APITestCase):
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

        self.offer_1 = Offer.objects.create(
            user=self.user_1,
            title="Website Design",
            description="Professionelles Website-Design...",
            min_price=1000,
            min_delivery_time=7,
        )

        self.offer_2 = Offer.objects.create(
            user=self.user_1,
            title="Website Design 2",
            description="Professionelles Website-Design...",
            min_price=100,
            min_delivery_time=70,
        )

        self.offer_3 = Offer.objects.create(
            user=self.user_1,
            title="Website Design 3",
            description="Professionelles Website-Design für den Test search...",
            min_price=10000,
            min_delivery_time=700,
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

        self.offer_detail_2 = OfferDetails.objects.create(
            offer_id=1,
            title="Standard Design",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=["Logo Design", "Visitenkarte", "Briefpapier"],
            offer_type="standard"
        )

        self.offer_detail_3 = OfferDetails.objects.create(
            offer_id=1,
            title="Premium Design",
            revisions=10,
            delivery_time_in_days=10,
            price=500,
            features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            offer_type="premium"
        )

    def test_offer_list_get_200(self):
        url = reverse("offer-list")
        response = self.user_client_1.get(url)

        expected_dict = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": OfferListSerializer(
                [self.offer_1, self.offer_2, self.offer_3],
                many=True,
                context={"request": response.wsgi_request}
            ).data
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_list_filter_by_creator_id_get_200(self):
        url = reverse("offer-list") + f"?creator_id={self.user_1.id}"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_dict = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": OfferListSerializer(
                [self.offer_1, self.offer_2, self.offer_3],
                many=True,
                context={"request": response.wsgi_request}
            ).data
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

    def test_offer_list_filter_by_creator_id_get_400(self):
        url = reverse("offer-list") + f"?creator_id={99}"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_list_filter_by_min_price_get_200(self):
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
            "results": OfferListSerializer(
                [self.offer_1, self.offer_2, self.offer_3],
                many=True,
                context={"request": response.wsgi_request}
            ).data
        }
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_list_filter_by_max_delivery_time_get_200(self):
        url = reverse("offer-list") + f"?max_delivery_time=7"
        response = self.user_client_1.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_dict = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [OfferListSerializer(
                self.offer_1,
                context={"request": response.wsgi_request}).data,
            ]

        }
        self.assertDictEqual(response.json(), expected_dict)

        url = reverse("offer-list") + f"?max_delivery_time=70"
        response = self.user_client_1.get(url)

        expected_dict = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": OfferListSerializer(
                [self.offer_1, self.offer_2],
                many=True,
                context={"request": response.wsgi_request}
            ).data
        }
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_list_ordering_min_price_get_200(self):
        url = reverse("offer-list") + f"?ordering=min_price"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_dict = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": OfferListSerializer(
                [self.offer_2, self.offer_1, self.offer_3],
                many=True,
                context={"request": response.wsgi_request}
            ).data
        }
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_list_ordering_updated_at_get_200(self):
        url = reverse("offer-list") + f"?ordering=updated_at"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_dict = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": OfferListSerializer(
                [self.offer_1, self.offer_2, self.offer_3],
                many=True,
                context={"request": response.wsgi_request}
            ).data
        }
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_list_search_title_get_200(self):
        url = reverse("offer-list") + f"?search=Design 3"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_dict = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [OfferListSerializer(
                self.offer_3,
                context={"request": response.wsgi_request}
            ).data]
        }
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_list_search_description_get_200(self):
        url = reverse("offer-list") + f"?search=Test"
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_dict = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [OfferListSerializer(
                self.offer_3,
                context={"request": response.wsgi_request}
            ).data]
        }
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_post_201(self):
        url = reverse("offer-list")
        payload = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                     "title": "Basic Design",
                     "revisions": 2,
                     "delivery_time_in_days": 5,
                     "price": 100,
                     "features": [
                         "Logo Design",
                         "Visitenkarte"
                     ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.user_client_1.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        expected_data = {
            "id": data["id"],
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "id": data["details"][0]["id"],
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                        "Visitenkarte"
                    ],
                    "offer_type": "basic"
                },
                {
                    "id": data["details"][1]["id"],
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "id": data["details"][2]["id"],
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }

        self.assertDictEqual(data, expected_data)

    def test_offer_post_missing_details_400(self):
        url = reverse("offer-list")
        payload = {"title": "Grafikdesign-Paket",
                   "image": None,
                   "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
                   "details": [
                       {
                           "title": "Basic Design",
                           "revisions": 2,
                           "delivery_time_in_days": 5,
                           "price": 100,
                           "features": [
                            "Logo Design",
                            "Visitenkarte"
                           ],
                           "offer_type": "basic"
                       },
                       {
                           "title": "Standard Design",
                           "revisions": 5,
                           "delivery_time_in_days": 7,
                           "price": 200,
                           "features": [
                               "Logo Design",
                               "Visitenkarte",
                               "Briefpapier"
                           ],
                           "offer_type": "standard"
                       },

                   ]
                   }
        response = self.user_client_1.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_post_400(self):
        url = reverse("offer-list")

        required_fields = ["title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]
        base_payload = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        }

        for field in required_fields:
            payload_missing_field = base_payload.copy()
            payload_missing_field["details"] = [d.copy() for d in base_payload["details"]]
            payload_missing_field["details"][0].pop(field)
            response = self.user_client_1.post(url, payload_missing_field, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, str(response.data))

    def test_offer_post_401(self):
        url = reverse("offer-list")
        data = {
            "user": self.user_2.id,
            "title": "New Offer",
            "description": "This is a new offer.",
            "min_price": 500,
            "min_delivery_time": 5,
        }
        self.user_client_1.logout()
        response = self.user_client_1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_post_403(self):
        url = reverse("offer-list")
        payload = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                           "title": "Basic Design",
                           "revisions": 2,
                           "delivery_time_in_days": 5,
                           "price": 100,
                           "features": [
                               "Logo Design",
                               "Visitenkarte"
                           ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.user_client_2.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_detail_get_200(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer_1.id})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        expected_dict = {
            "id": data["id"],
            "user": data["user"],
            "title": "Website Design",
            "image": None,
            "description": "Professionelles Website-Design...",
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "details": data["details"],
            "min_price": 1000,
            "min_delivery_time": 7
        }

        self.assertDictEqual(data, expected_dict)

    def test_offer_detail_get_401(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer_1.id})
        self.user_client_1.logout()
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_get_404(self):
        url = reverse("offer-detail", kwargs={"pk": 9999999})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_detail_get_404(self):
        url = reverse("offer-detail", kwargs={"pk": 9999999})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_detail_patch_200(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer_1.id})
        payload = {
            "title": "Updated Grafikdesign-Paket",
            "details": [
                {
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": [
                        "Logo Design",
                        "Flyer"
                    ],
                    "offer_type": "basic"
                }
            ]
        }
        response = self.user_client_1.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        expected_dict = {
            "id": data["id"],
            "title": "Updated Grafikdesign-Paket",
            "image": None,
            "description": self.offer_1.description,
            "details": [
                {
                    "id": data["details"][0]["id"],
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": [
                        "Logo Design",
                        "Flyer"
                    ],
                    "offer_type": "basic"
                },
                {
                    "id": data["details"][1]["id"],
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier"
                    ],
                    "offer_type": "standard"
                },
                {
                    "id": data["details"][2]["id"],
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer"
                    ],
                    "offer_type": "premium"
                }
            ]

        }
        self.assertDictEqual(data, expected_dict)

    def test_offer_detail_patch_400(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer_1.id})

        payload = {'title': ""}
        response = self.user_client_1.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        details_required_fields = [
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type"
        ]

        for field in details_required_fields:
            payload = {
                "details": [
                    {
                        "title": "Basic Design Updated",
                        "revisions": 3,
                        "delivery_time_in_days": 6,
                        "price": 120,
                        "features": ["Logo Design", "Flyer"],
                        "offer_type": "basic"
                    }
                ]
            }
            payload["details"][0].pop(field)

            response = self.user_client_1.patch(url, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, str(response.data))

    def test_offer_detail_patch_401(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer_1.id})
        payload = {
            "title": "Updated Grafikdesign-Paket",
        }
        self.user_client_1.logout()
        response = self.user_client_1.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_patch_403(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer_1.id})
        payload = {
            "title": "Updated Grafikdesign-Paket",
        }
        response = self.user_client_2.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_detail_patch_404(self):
        url = reverse("offer-detail", kwargs={"pk": 9999})
        payload = {
            "title": "Updated Grafikdesign-Paket",
        }
        response = self.user_client_1.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_offer_detail_delete_204(self):
        url = reverse("offer-detail", kwargs={"pk": self.offer_1.id})
        response = self.user_client_1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_offer_details_detail_get_200(self):
        url = reverse("offer-details", kwargs={"pk": self.offer_detail_1.id})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_dict = {
            "id": self.offer_detail_1.id,
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": ["Logo Design", "Visitenkarte"],
            "offer_type": "basic"
        }
        self.assertDictEqual(response.json(), expected_dict)

    def test_offer_details_detail_get_401(self):
        url = reverse("offer-details", kwargs={"pk": self.offer_detail_1.id})
        self.user_client_1.logout()
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_details_detail_get_404(self):
        url = reverse("offer-details", kwargs={"pk": 9999})
        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User
from app_reviews.models import Review


class TestProfiles(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="jdoe", password="examplePassword", email="test@test.de", type="customer", first_name="John", last_name="Doe")
        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.user_client_1 = APIClient()
        self.user_client_1.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1.key)

        self.user_2 = User.objects.create_user(
            username="mschaar", password="examplePassword", email="test2@test.de", type="business", first_name="Marc", last_name="Schaar")
        self.token_user_2 = Token.objects.create(user=self.user_2)
        self.user_client_2 = APIClient()
        self.user_client_2.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_2.key)

        self.user_3 = User.objects.create_user(
            username="user3", password="examplePassword", email="test3@test.de", type="customer", first_name="Marc", last_name="Schaar")
        self.token_user_3 = Token.objects.create(user=self.user_3)
        self.user_client_3 = APIClient()
        self.user_client_3.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_3.key)

        self.user_4 = User.objects.create_user(
            username="user4", password="examplePassword", email="test4@test.de", type="customer", first_name="Marc", last_name="Schaar")
        self.token_user_4 = Token.objects.create(user=self.user_4)
        self.user_client_4 = APIClient()
        self.user_client_4.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_4.key)

        self.user_5 = User.objects.create_user(
            username="user5", password="examplePassword", email="test5@test.de", type="business", first_name="Marc", last_name="Schaar")
        self.token_user_5 = Token.objects.create(user=self.user_5)
        self.user_client_5 = APIClient()
        self.user_client_5.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_5.key)

        self.user_6 = User.objects.create_user(
            username="user6", password="examplePassword", email="test6@test.de", type="business", first_name="Marc", last_name="Schaar")
        self.token_user_6 = Token.objects.create(user=self.user_6)
        self.user_client_6 = APIClient()
        self.user_client_6.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_6.key)

        self.review_1 = Review.objects.create(
            business_user=self.user_2,
            reviewer=self.user_3,
            rating=4,
            description="Sehr professioneller Service.",
        )

        self.review_2 = Review.objects.create(
            business_user=self.user_5,
            reviewer=self.user_3,
            rating=5,
            description="Top Qualität und schnelle Lieferung!",
        )


class TestReviews(TestProfiles):
    maxDiff = None

    def test_review_list(self):
        url = reverse("reviews-list")
        response = self.user_client_1.get(url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 1,
                "business_user": 2,
                "reviewer": 3,
                "rating": 4,
                "description": "Sehr professioneller Service.",
            },
            {
                "id": 2,
                "business_user": 5,
                "reviewer": 3,
                "rating": 5,
                "description": "Top Qualität und schnelle Lieferung!",
            }
        ]

        cleaned_response = [
            {
                "id": r["id"],
                "business_user": r["business_user"],
                "reviewer": r["reviewer"],
                "rating": r["rating"],
                "description": r["description"]
            }
            for r in response_data
        ]
        self.assertEqual(cleaned_response, expected_data)

        for r in response_data:
            self.assertIn('created_at', r)
            self.assertIn('updated_at', r)

    def test_offer_list_401(self):
        url = reverse("reviews-list")
        self.user_client_1.logout()

        response = self.user_client_1.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_list_filtered_by_business_user_id(self):
        url = reverse("reviews-list") + f"?business_user_id={self.user_2.id}"
        response = self.user_client_1.get(url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 1,
                "business_user": 2,
                "reviewer": 3,
                "rating": 4,
                "description": "Sehr professioneller Service.",
            },
        ]

        cleaned_response = [
            {
                "id": r["id"],
                "business_user": r["business_user"],
                "reviewer": r["reviewer"],
                "rating": r["rating"],
                "description": r["description"]
            }
            for r in response_data
        ]
        self.assertEqual(cleaned_response, expected_data)

    def test_review_list_filtered_by_reviewer_id(self):
        url = reverse("reviews-list") + f"?reviewer_id={self.user_3.id}"
        response = self.user_client_1.get(url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 1,
                "business_user": 2,
                "reviewer": 3,
                "rating": 4,
                "description": "Sehr professioneller Service.",
            },
            {
                "id": 2,
                "business_user": 5,
                "reviewer": 3,
                "rating": 5,
                "description": "Top Qualität und schnelle Lieferung!",
            }
        ]

        cleaned_response = [
            {
                "id": r["id"],
                "business_user": r["business_user"],
                "reviewer": r["reviewer"],
                "rating": r["rating"],
                "description": r["description"]
            }
            for r in response_data
        ]
        self.assertEqual(cleaned_response, expected_data)

    def test_review_list_ordered_by_reviewer_id(self):
        url = reverse("reviews-list") + f"?ordering={'-rating'}"
        response = self.user_client_1.get(url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 2,
                "business_user": 5,
                "reviewer": 3,
                "rating": 5,
                "description": "Top Qualität und schnelle Lieferung!",
            },
            {
                "id": 1,
                "business_user": 2,
                "reviewer": 3,
                "rating": 4,
                "description": "Sehr professioneller Service.",
            }

        ]

        cleaned_response = [
            {
                "id": r["id"],
                "business_user": r["business_user"],
                "reviewer": r["reviewer"],
                "rating": r["rating"],
                "description": r["description"]
            }
            for r in response_data
        ]
        self.assertEqual(cleaned_response, expected_data)

    def test_review_post_201(self):
        url = reverse('reviews-list')
        payload = {
            "business_user": self.user_6.id,
            "rating": 4,
            "description": "Alles war toll!"
        }

        response = self.user_client_3.post(url, payload)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['id'], 3)
        self.assertEqual(response_data['business_user'], 6)
        self.assertEqual(response_data['reviewer'], 3)
        self.assertEqual(response_data['rating'], 4)
        self.assertEqual(response_data['description'], "Alles war toll!")
        self.assertIn('created_at', response_data)
        self.assertIn('updated_at', response_data)

    def test_review_post_missing_fields_400(self):
        url = reverse('reviews-list')
        missing_field_payloads = [
            {"rating": 4, "description": "Alles war toll!"},
            {"business_user": self.user_2.id, "description": "Alles war toll!"},
            {"business_user": self.user_5.id, "rating": 4},
        ]

        for p in missing_field_payloads:
            response = self.user_client_3.post(url, p, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_post_duplicate_400(self):
        url = reverse('reviews-list')
        payload = {"business_user": self.user_2.id, "rating": 2, "description": "Nicht toll!"}
        self.user_client_3.post(url, payload, format='json')
        response = self.user_client_3.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_post_401(self):
        url = reverse('reviews-list')
        payload = {"business_user": self.user_2.id, "rating": 2, "description": "Nicht toll!"}
        self.user_client_3.logout()
        response = self.user_client_3.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_post_403(self):
        url = reverse('reviews-list')
        payload = {"business_user": self.user_2.id, "rating": 2, "description": "Nicht toll!"}
        response = self.user_client_6.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_patch_200(self):
        url = reverse('reviews-detail', kwargs={"pk": self.review_1.id})
        payloads = [
            {"rating": 1},
            {"description": "Sehr  unprofessioneller Service."},
        ]
        for payload in payloads:
            response = self.user_client_3.patch(url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.review_1.refresh_from_db()

            for key, value in payload.items():
                self.assertEqual(getattr(self.review_1, key), value)

    def test_review_patch_400(self):
        url = reverse('reviews-detail', kwargs={"pk": self.review_1.id})
        invalid_payloads = [
            {"business_user": 1},
            {"reviewer": 3},
            {"created_at": "2024-01-01T00:00:00Z"},
            {"updated_at": "2024-01-01T00:00:00Z"},

        ]
        for payload in invalid_payloads:
            response = self.user_client_3.patch(url, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_patch_401(self):
        url = reverse('reviews-detail', kwargs={"pk": self.review_1.id})
        payload = {"business_user": 1},
        self.user_client_3.logout()

        response = self.user_client_3.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_patch_403(self):
        url = reverse('reviews-detail', kwargs={"pk": self.review_1.id})
        payload = {"rating": 1}

        response = self.user_client_1.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

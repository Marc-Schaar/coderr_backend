from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from app_accounts.models import User, Profile
from app_accounts.api.serializers import ProfileDetailSerializer, ProfileListSerializer


class TestProfiles(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username="max_mustermann",
            password="examplePassword",
            email="test@test.de",
            type="business",
        )
        self.user_2 = User.objects.create_user(
            username="exampleUsername_2",
            password="examplePassword",
            email="email2est,de",
            type="customer",
        )

        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.token_user_2 = Token.objects.create(user=self.user_2)

        self.user_client_1 = APIClient()
        self.user_client_1.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_user_1.key
        )

        self.user_client_2 = APIClient()
        self.user_client_2.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_user_2.key
        )

    def test_profile_get_200_as_business_user(self):
        url = reverse("profile-detail", kwargs={"pk": self.user_1.id})
        response = self.user_client_1.get(url, format="json")
        expected_data = ProfileDetailSerializer(self.user_1.profile).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected_data)

    def test_profile_get_200_as_customer_user(self):
        url = reverse("profile-detail", kwargs={"pk": self.user_2.id})
        response = self.user_client_2.get(url, format="json")
        expected_data = ProfileDetailSerializer(self.user_2.profile).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), expected_data)

    def test_profile_detail_get_401(self):
        url = reverse("profile-detail", kwargs={"pk": self.user_1.pk})
        self.user_client_1.logout()

        response = self.user_client_1.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_get_404_(self):
        url = reverse("profile-detail", kwargs={"pk": 999999})
        response = self.user_client_1.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_detail_patch_200(self):
        url = reverse("profile-detail", kwargs={"pk": 1})
        payload = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de",
        }

        response = self.user_client_1.patch(url, payload, format="json")
        self.user_1.refresh_from_db()
        self.user_1.profile.refresh_from_db()
        expected_data = ProfileDetailSerializer(self.user_1.profile).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, expected_data)
        self.assertEqual(self.user_1.profile.location, "Berlin")
        self.assertEqual(self.user_1.profile.tel, "987654321")
        self.assertEqual(
            self.user_1.profile.description, "Updated business description"
        )
        self.assertEqual(self.user_1.profile.working_hours, "10-18")
        self.assertEqual(self.user_1.first_name, "Max")
        self.assertEqual(self.user_1.last_name, "Mustermann")
        self.assertEqual(self.user_1.email, "new_email@business.de")

    def test_profile_detail_patch_401(self):
        url = reverse("profile-detail", kwargs={"pk": 1})
        payload = {
            "first_name": "Max",
        }
        self.user_client_1.logout()
        response = self.user_client_1.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_patch_403(self):
        url = reverse("profile-detail", kwargs={"pk": 1})
        payload = {
            "first_name": "Max",
        }
        response = self.user_client_2.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_patch_404(self):
        url = reverse("profile-detail", kwargs={"pk": 999999})
        payload = {
            "first_name": "Max",
        }
        response = self.user_client_1.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_get_business_list_200(self):
        url = reverse(
            "profile-business-list",
        )
        response = self.user_client_1.get(url, format="json")
        expected_data = ProfileListSerializer(
            Profile.objects.filter(user__type="business"), many=True
        ).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), expected_data)
        self.assertIn('user', response.json()[0])
        self.assertIn('username', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('file', response.json()[0])
        self.assertIn('location', response.json()[0])
        self.assertIn('tel', response.json()[0])
        self.assertIn('description', response.json()[0])
        self.assertIn('type', response.json()[0])
        self.assertIn('working_hours', response.json()[0])

    def test_profile_get_business_list_401(self):
        url = reverse("profile-business-list")
        self.user_client_1.logout()
        response = self.user_client_1.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_get_customer_list_200(self):
        url = reverse(
            "profile-customer-list",
        )
        response = self.user_client_1.get(url, format="json")
        expected_data = ProfileListSerializer(
            Profile.objects.filter(user__type="customer"), many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), expected_data)
        self.assertIn('user', response.json()[0])
        self.assertIn('username', response.json()[0])
        self.assertIn('first_name', response.json()[0])
        self.assertIn('last_name', response.json()[0])
        self.assertIn('file', response.json()[0])
        self.assertIn('type', response.json()[0])

    def test_profile_get_business_list_401(self):
        url = reverse("profile-customer-list")
        self.user_client_1.logout()
        response = self.user_client_1.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

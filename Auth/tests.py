import requests
from django.test import TestCase
from dotenv import dotenv_values
from firebase_admin import auth
from rest_framework.test import APIRequestFactory, force_authenticate

from Auth.views import LoginAPI, LogoutAPI, ProfileAPI
from User.models import User

ENV = dotenv_values(".env.test")
FIREBASE_TEST_UID = ENV.get("FIREBASE_TEST_UID")
FIREBASE_API_KEY = ENV.get("FIREBASE_API_KEY")
FIREBASE_API_URL = ENV.get("FIREBASE_API_URL")
FIREBASE_TEST_USER_EMAIL = ENV.get("FIREBASE_TEST_USER_EMAIL")

factory = APIRequestFactory()


def get_valid_id_token(
    user_id=FIREBASE_TEST_UID,
):
    token = auth.create_custom_token(user_id)

    url = f"{FIREBASE_API_URL}?key={FIREBASE_API_KEY}"
    response = requests.post(url, {"token": token, "returnSecureToken": True})

    return response.json().get("idToken")


class AuthTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            email=FIREBASE_TEST_USER_EMAIL,
            username="Test User",
            profile_image="https://picsum.photos/512",
            is_active=True,
        )
        return super().setUp()

    @staticmethod
    def perform_auth_request(self, id_token: str):
        request = factory.post(
            "/api/auth/login",
            {"id_token": id_token},
            format="json",
        )
        view = LoginAPI.as_view()

        return view(request)

    def test_login_invalid_id_token(self):
        response = self.perform_auth_request("Malformed ID Token")
        self.assertEqual(response.status_code, 400)

    def test_login_valid_id_token(self):
        id_token = get_valid_id_token()
        response = self.perform_auth_request(id_token)

        self.assertEqual(response.status_code, 200)

        if response.data is None:
            return self.fail("Data is None")

        self.assertIsNotNone(response.data["access_token"])
        self.assertIsNotNone(response.data["refresh_token"])

    def test_get_user_profile(self):
        user = User.objects.get(email=FIREBASE_TEST_USER_EMAIL)
        request = factory.get("/api/auth/profile")
        force_authenticate(request, user=user)

        view = ProfileAPI.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["id"])
        self.assertIsNotNone(response.data["email"])
        self.assertIsNotNone(response.data["username"])
        self.assertIsNotNone(response.data["profile_image"])
        self.assertIsNotNone(response.data["is_active"])

    def test_logout(self):
        user = User.objects.get(email=FIREBASE_TEST_USER_EMAIL)
        request = factory.post("/api/auth/logout", {})
        force_authenticate(request, user=user)

        view = LogoutAPI.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 205)

import json
from urllib.parse import urlencode

import responses
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from rae.helpers import send_data_to_ceremeo
from rae.models import BusinessCard


class TestBusinessCard(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.bc_logged = BusinessCard.objects.create_user(username="test_bc", password="password")
        cls.url_generate_data = reverse("generate-data")
    def setUp(self):
        self.client = Client()

    def test_get_generate_data_not_logged_cannot_enter(self):
        """
        Not logged-in user is not allowed to enter the page.
        """
        # Act
        response = self.client.get(self.url_generate_data)
        redirect_url = f"{reverse('login')}?{urlencode({'next': self.url_generate_data})}"

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_get_generate_data_logged_in_user_can_enter(self):
        """
        Logged-in user is allowed to enter the page.
        """
        # Arrange
        self.client.force_login(user=self.bc_logged)

        # Act
        response = self.client.get(self.url_generate_data)

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_post_get_generate_data_save_to_db(self):
        """
        Send data should update the BusinessCard object.
        """
        # Arrange
        self.client.force_login(user=self.bc_logged)
        data = {
            "name": "Jan Kowalski",
            "company": "Firma Test",
            "phone": "123-123-123",
            "url": "jankowalski",
        }

        # Act
        response = self.client.post(self.url_generate_data, data=data)

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("display-data"))
        data["url"] = f"https://card.ceremeo.pl/{data['url']}"
        self.assertTrue(BusinessCard.objects.filter(**data).exists())


@override_settings(CEREMEO_API_KEY="test123")
class TestAPICeremeo(TestCase):
    URL = "https://api.ceremeo.pl/test"
    REQUEST_DATA = {
        "phone": "123456789",
        "name": "Piotr Nowak",
        "company": "Firma Test",
        "date": "01.02.2025",
        "subject": "Oferta zakupu aplikacji",
    }
    RESPONSE_DATA = {"key": "success"}
    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token test123",
    }

    @responses.activate
    def test_success_api_data(self):
        # Arrange
        responses.add(
            method=responses.POST,
            url=self.URL,
            json=self.RESPONSE_DATA,
            status=200,
        )

        # Act
        result = send_data_to_ceremeo(payload=self.REQUEST_DATA, url=self.URL)

        # Arrange
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(json.loads(responses.calls[0].request.body), self.REQUEST_DATA)
        self.assertEqual(result, self.RESPONSE_DATA)

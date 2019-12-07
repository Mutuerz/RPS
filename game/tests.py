from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
import json


class GameTests(APITestCase, URLPatternsTestCase):
    def test_start_game(self):
        url = reverse('list-games')
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), {"links": {"next": None, "previous": None}})

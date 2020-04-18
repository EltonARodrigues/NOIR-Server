from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse, resolve
from rest_framework import status
from datetime import datetime
import json
import uuid

client = APIClient()


class GasesCollectedTestCase(TestCase):

    def setUp(self):
        self.uri = '/api/gases/'
        now = datetime.now()
        self.value = {
                        "id": "789ed3a4-85a8-476e-bff5-fb6899e74f16",
                        "created_at": now.strftime("%Y-%m-%dT%H:%MZ"),
                        "temperature": 55.0,
                        "humidity": 58.0,
                        "co": 55.58,
                        "co2": 44.5,
                        "mp25": 55.5,
                        "sensor": "4d4ca279-d266-4506-b749-0c19215f0655"
                    }

    def test_post_gases(self):
        response = client.post(self.uri,
                                data=json.dumps(self.value),
                                content_type='text/csv'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_gases(self):
        response = client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SensorViewSetTestCase(TestCase):

    def setUp(self):
        now = datetime.now()
        self.uri = '/api/sensors/'
        self.value = {
                        "title": str(uuid.uuid4())[:8],
                        "description": str(uuid.uuid4())[:8],
                        "author": 1
                    }

    def test_post_sensor(self):
        response = client.post(self.uri,
                                data=json.dumps(self.value),
                                content_type='application/json')

        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_gases(self):
        response = client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)